from flask import Flask
from flask_wtf import CSRFProtect
from exts import db, aliyunsms
import config
from apps.cms.views import bp as cms
from apps.common.views import bp as common
from apps.front.views import bp as front
from apps.ueditor import bp as ueditor

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


if __name__ == '__main__':
    # app.run(port=8000, ssl_context='adhoc')
    app.run(port=8000)
