from flask import Blueprint, render_template, views, request, redirect, url_for, session, g
from .forms import LoginForm
from .models import CMSUser
from .decorators import login_required
import config

# bp = Blueprint('cms', __name__, subdomain='cms')
bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    # 源码:http://www.17sucai.com/pins/21355.html
    return render_template('cms/cms_base.html')

@bp.route('/first/')
def findex():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
def logout():
    session.pop(config.CMS_USER_ID)
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
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
            error_msg = form.errors.popitem()[1][0]
            return self.get(message=error_msg)


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session[config.CMS_USER_ID]
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
