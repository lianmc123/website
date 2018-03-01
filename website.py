from flask import Flask
from flask_wtf import CSRFProtect
from exts import db, mail
import config
from apps.cms.views import bp as cms
from apps.common.views import bp as common
from apps.front.views import bp as front


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)
app.register_blueprint(cms)
app.register_blueprint(common)
app.register_blueprint(front)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run(port=8000, ssl_context='adhoc')
    app.run(port=8000)
