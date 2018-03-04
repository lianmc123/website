from flask import Blueprint, views, render_template, request, session, url_for
from .forms import SignupForm, SigninForm
from .models import FrontUser
from exts import db
from utils import restful, safeurl
import config

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    # http://www.17sucai.com/preview/1/2016-01-26/LineMenuStyles/index.html
    return render_template('front/front_index.html')


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
