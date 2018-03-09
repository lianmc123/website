from flask import Blueprint, render_template, views, request, redirect, url_for, session, g, jsonify
from .forms import LoginForm, ResetPwdForm, ResetEmailForm, AddBannerForm, UpdateBannerForm, AddBoardForm, \
    UpdateBoardForm
from .models import CMSUser, CMSPermission
from apps.common.models import BannerModel, BoardModel, PostModel, HighlightPostModel
from .decorators import login_required, permission_required
import config
from exts import db, mail
from utils import restful, web_cache
from flask_mail import Message
import string
import random
from flask_paginate import Pagination, get_page_parameter
from tasks import send_mail

# bp = Blueprint('cms', __name__, subdomain='cms')
bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    # 源码:http://www.17sucai.com/pins/21355.html
    return render_template('cms/cms_base.html')


@bp.route('/first/')
@login_required
def findex():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
def logout():
    session.pop(config.CMS_USER_ID)
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 30
    end = start + 30
    total = PostModel.query.count()
    context = {
        'posts': PostModel.query.slice(start, end),
        'pagination': Pagination(bs_version=3, page=page, total=total, outer_window=0, per_page=30)
    }
    return render_template('cms/cms_posts.html', **context)


@bp.route('/spost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def spost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error("Post_id不存在")
    post = PostModel.query.get(post_id)
    if post:
        post_show = post.is_show
        if post_show == 0:
            post.is_show = 1
        else:
            post.is_show = 0
        db.session.commit()
        return restful.success()
    else:
        restful.params_error("Post未找到")


@bp.route('/dpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error("Post_id不存在")
    post = PostModel.query.get(post_id)
    if post:
        # db.session.delete(post)
        # db.session.commit()
        print('删除帖子成功')
        return restful.success()
    else:
        restful.params_error("Post未找到")


@bp.route('/hpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("帖子不存在")
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/uhpost/', methods=["POST"])
@login_required
@permission_required(CMSPermission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子id")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("帖子不存在")
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    board_models = BoardModel.query.all()
    return render_template('cms/cms_boards.html', boards=board_models)


@bp.route('/aboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.error_msg())


@bp.route('/uboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error("未找到板块")
    else:
        return restful.params_error(form.error_msg())


@bp.route('/sboard/', methods=["POST"])
@login_required
@permission_required(CMSPermission.BOARDER)
def sboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error("Board_id不存在")
    board = BoardModel.query.get(board_id)
    if board:
        board_show = board.is_show
        if board_show == 0:
            board.is_show = 1
        else:
            board.is_show = 0
        db.session.commit()
        return restful.success()
    else:
        restful.params_error("Board未找到")


@bp.route('/dboard/', methods=['POST'])
@login_required
def dboard():
    board_id = request.form.get('board_id')
    if not board_id:
        return restful.params_error("Board_id不存在")
    board = BoardModel.query.get(board_id)
    if board:
        # db.session.delete(board)
        # db.session.commit()
        print("删除成功")
        return restful.success()
    else:
        restful.params_error("Board未找到")


@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/banners/')
@login_required
def banners():
    # http://www.htmleaf.com/jQuery/Buttons-Icons/201502051331.html  # bootstrap 开关
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


class LoginView(views.MethodView):
    def get(self, message=None):
        # 源码:https://v3.bootcss.com/examples/signin/
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(raw_password=password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            error_msg = form.error_msg()
            return self.get(message=error_msg)


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.error_msg())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    @login_required
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            user = g.cms_user
            user.email = form.email.data
            db.session.commit()
            # web_cache.Memcache().set(form.email.data, "asd.")
            web_cache.RedisCache().set(form.email.data, "asd.")
            return restful.success()
        else:
            return restful.params_error(form.error_msg())


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.error_msg())


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error("未找到Banner")
    else:
        return restful.params_error(form.error_msg())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error("Banner_id不存在")
    banner = BannerModel.query.get(banner_id)
    if banner:
        # db.session.delete(banner)
        # db.session.commit()
        print("删除成功")
        return restful.success()
    else:
        restful.params_error("Banner未找到")


@bp.route('/sbanner/', methods=['POST'])
@login_required
def sbanner():
    banner_id = request.form.get('banner_id')
    print(banner_id)
    if not banner_id:
        return restful.params_error("Banner_id不存在")
    banner = BannerModel.query.get(banner_id)
    if banner:
        banner_show = banner.is_show
        if banner_show == 0:
            banner.is_show = 1
        else:
            banner.is_show = 0
        db.session.commit()
        return restful.success()
    else:
        restful.params_error("Banner未找到")


@bp.route('/email_captcha/')
@login_required
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error("请传递正确的邮箱")
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 4))
    # message = Message(subject='验证码', recipients=[email],
    #                   body="邮箱内容: %s(30分钟有效)" % captcha)
    # try:
    #     # mail.send(message)
    #     # web_cache.Memcache().set(email, captcha)
    #     web_cache.RedisCache().set(email, captcha)
    # except Exception as ex:
    #     return restful.server_error("出错了")
    send_mail.delay('验证码', [email], "邮箱内容: %s(30分钟有效)" % captcha)
    web_cache.RedisCache().set(email, captcha)
    return restful.success()


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session[config.CMS_USER_ID]
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
