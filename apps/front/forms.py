from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import EqualTo, Regexp, Length

class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确的手机号码!")])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}', message="短信验证码错误!")])
    username = StringField(validators=[Regexp(r".{2,20}", message="username error")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6, 20}")])
    password1 = StringField(validators=EqualTo("password", message="double pasword no equal"))