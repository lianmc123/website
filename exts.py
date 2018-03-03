from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
# from utils.alidayu import AlidayuAPI
from utils.aliyunsms import AliYunSMS

db = SQLAlchemy()
mail = Mail()
# alidayu = AlidayuAPI()
aliyunsms = AliYunSMS()