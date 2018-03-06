from flask import Blueprint, views, render_template, request, session, url_for, g
from .forms import SignupForm, SigninForm, AddPostForm
from .models import FrontUser
from apps.common.models import BannerModel, BoardModel, PostModel
from exts import db
from utils import restful, safeurl
import config
from .decorators import login_required

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # http://www.17sucai.com/preview/1/2016-01-26/LineMenuStyles/index.html
    banners = BannerModel.query.filter_by(is_show=1).order_by(BannerModel.priority.desc()).all()
    boards = BoardModel.query.filter_by(is_show=1).all()
    context = {
        "banners": banners,
        "boards": boards
    }
    return render_template('front/front_index.html', **context)


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
            if board:
                post = PostModel(title=title, content=content)
                post.board_id = board_id
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
