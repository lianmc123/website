from functools import wraps
from flask import session, redirect, url_for
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

