from flask import Blueprint, render_template, views, request, redirect, url_for, session, g, jsonify
from .forms import LoginForm, ResetPwdForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db
from utils import restful

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
    @login_required
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        pass


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
