from .views import bp
import config
from flask import session, g, render_template
from .models import FrontUser


@bp.before_request
def my_before_request():
    if config.FRONT_USER_ID in session:
        user_uid = session.get(config.FRONT_USER_ID)
        user = FrontUser.query.filter_by(uid=user_uid).first()
        if user:
            g.front_user = user


