from .views import bp
import config
from flask import session, g, redirect, url_for
from .models import CMSUser


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session[config.CMS_USER_ID]
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.app_errorhandler
def app_errorhandler():
    return redirect()