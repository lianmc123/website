from flask import Blueprint, views, render_template, request, session, url_for, g, abort
from .forms import SignupForm, SigninForm, AddPostForm, AddCommentForm
from .models import FrontUser
from apps.common.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel
from exts import db
from utils import restful, safeurl
import config
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import func

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # http://www.17sucai.com/preview/1/2016-01-26/LineMenuStyles/index.html
    board_id = request.args.get('bd', type=int, default=None)
    sort = request.args.get('st', type=int, default=1)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    banners = BannerModel.query.filter_by(is_show=1).order_by(BannerModel.priority.desc()).all()
    boards = BoardModel.query.filter_by(is_show=1).all()
    # g_posts = PostModel.query.join(BoardModel).filter(PostModel.is_show == 1, BoardModel.is_show == 1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    query_l = None
    if sort == 1:
        query_l = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        query_l = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        query_l = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        query_l = PostModel.query.join(CommentModel, isouter=True).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())
    if board_id:
        # query = PostModel.query.join(BoardModel).filter(PostModel.is_show == 1, BoardModel.is_show == 1,
        #                                                 PostModel.board_id == board_id)
        query = query_l.join(BoardModel).filter(PostModel.is_show == 1, BoardModel.is_show == 1,
                                                PostModel.board_id == board_id)
        posts = query.slice(start, end)
        total = query.count()
    else:
        # posts = g_posts.slice(start, end)
        # total = g_posts.count()
        query_l_b = query_l.join(BoardModel).filter(PostModel.is_show == 1, BoardModel.is_show == 1)
        posts = query_l_b.slice(start, end)
        total = query_l_b.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0)
    context = {
        "banners": banners,
        "boards": boards,
        "posts": posts,
        'pagination': pagination,
        'current_board_id': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)


@bp.route('/p/<post_id>/')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template("front/front_pdetail.html", post=post)


@bp.route('/acomment/', methods=["POST"])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error("找不到该文章")
    else:
        return restful.params_error(form.error_msg())


@bp.route('/add_post/', methods=["GET", "POST"])
@login_required
def add_post():
    if request.method == "GET":
        boards = BoardModel.query.filter_by(is_show=1).all()
        context = {
            "boards": boards
        }
        return render_template('front/front_ppost.html', **context)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            author = g.front_user
            if board:
                post = PostModel(title=title, content=content)
                post.board_id = board_id
                post.author = author
                db.session.add(post)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("板块不存在")
        else:
            return restful.params_error(form.error_msg())


class SignUpView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeurl.is_safe_url(return_to):
            return render_template("front/front_signup.html", return_to=return_to)
        else:
            return render_template("front/front_signup.html")

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password1.data
            username = form.username.data
            f_user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(f_user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.error_msg())


class SignInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeurl.is_safe_url(return_to) and return_to != url_for(
                'front.signup'):
            return render_template("front/front_signin.html", return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            print(remember)
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.uid
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(msg="手机号码或密码错误!")
        else:
            return restful.params_error(msg=form.error_msg())


bp.add_url_rule("/signup/", view_func=SignUpView.as_view("signup"))
bp.add_url_rule("/signin/", view_func=SignInView.as_view("signin"))
