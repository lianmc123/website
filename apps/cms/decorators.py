from functools import wraps
from flask import session, redirect, url_for, g
import config


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get(config.CMS_USER_ID, None)
        if user_id:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = g.cms_user
            if user and user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))

        return wrapper

    return outter
