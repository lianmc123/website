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
SECRET_KEY = os.urandom(24)
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
# ----------------- 分割线 ---------------------

# ----------------- 常量 ---------------------
CMS_USER_ID = "ASDGFSDF"
# ----------------- 分割线 ---------------------
