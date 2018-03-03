import os
from datetime import timedelta

# ------------ app.run()相关参数---------------
DEBUG = True
# ----------------- 分割线 --------------------

# ------------- SQLAlchemy 相关----------------
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DATABASE = 'website'
DB_USERNAME = 'root'
DB_PASSWORD = '124578'
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}" \
         "?charset=utf8".format(username=DB_USERNAME,
                                password=DB_PASSWORD, host=DB_HOST,
                                port=DB_PORT, db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# ----------------- 分割线 ---------------------

# -------------- session相关 -------------------
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "a6sd51as5d1asd66"
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
# ----------------- 分割线 ---------------------

# ----------------- 常量 -----------------------
CMS_USER_ID = "ASDGFSDF"
# ----------------- 分割线 ---------------------

# ----------------- 邮箱 -----------------------
MAIL_SERVER = "smtp.126.com"
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = "q135025@126.com"
MAIL_PASSWORD = "bnmbnm123123"
MAIL_DEFAULT_SENDER = "q135025@126.com"
MAIL_DEBUG = False
# ----------------- 分割线 ---------------------

# ----------------- 阿里大于 -----------------------
ALIDAYU_APP_KEY = 'LTAIfbaYxJm4sWQZ'
ALIDAYU_APP_SECRET = 'K8q1CPvkFNYeRuMqIMtlQUfBDWBJNv'
# ALIDAYU_APP_SECRET = 'K8q1CPvkFNYeRuMqIMtlQUfBDWBJNn'
ALIDAYU_SIGN_NAME = '易秀米'
ALIDAYU_TEMPLATE_CODE = 'SMS_126635198'
# ----------------- 分割线 ---------------------

# ----------------- 短信验证码 -----------------------
SMS_SALT = "sodhfoaw201rkqwuhro"
# ----------------- 分割线 ---------------------
