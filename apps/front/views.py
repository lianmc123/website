from flask import Blueprint

bp = Blueprint('front', __name__)


@bp.route('/front')
def index():
    return 'front index'