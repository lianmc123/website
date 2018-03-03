from flask import Blueprint, views, render_template

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    return 'front index'


class SignUpView(views.MethodView):
    def get(self):
        return render_template("front/front_signup.html")

    def post(self):
        return '成功'


bp.add_url_rule("/signup/", view_func=SignUpView.as_view("signup"))
