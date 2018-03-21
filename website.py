from flask import Flask, render_template
from flask_wtf import CSRFProtect
from exts import db, aliyunsms
import config
from apps.cms.views import bp as cms
from apps.common.views import bp as common
from apps.front.views import bp as front
from apps.ueditor import bp as ueditor
import datetime

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
aliyunsms.init_app(app)
CSRFProtect(app)
app.register_blueprint(cms)
app.register_blueprint(common)
app.register_blueprint(front)
app.register_blueprint(ueditor)



# @app.route('/')
# def hello_world():
#     return 'Hello World!'

@app.template_filter('handle_time')
def xxxx(value):
    if isinstance(value, datetime.datetime):
        now = datetime.datetime.now()
        now_value = (now - value).total_seconds()
        if now_value < 60:
            return '刚刚'
        elif now_value < 3600:
            return '%d分钟前' % (now_value // 60)
        elif now_value < 86400:
            return '%d小时前' % (now_value // 3600)
        elif now_value < 60 * 60 * 24 * 365:
            return '%d天前' % int(now_value / (3600 * 24))
        else:
            return value.strftime('%Y-%m-%d')
    else:
        return ''


@app.errorhandler(404)
def page_not_found(error):
    return render_template('front/front_404.html'), 404


if __name__ == '__main__':
    # app.run(port=8000, ssl_context='adhoc')
    app.run(port=8006)
