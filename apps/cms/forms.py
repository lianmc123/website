from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo, ValidationError
from ..forms import BaseForm
from utils import web_cache
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式错误"), InputRequired(message="邮箱不能为空")])
    password = StringField(validators=[Length(min=6, max=16, message="密码长度错误")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(min=6, max=16, message="旧密码格式错误")])
    newpwd = StringField(validators=[Length(min=6, max=16, message="新密码格式错误")])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入不一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式错误")])
    captcha = StringField(validators=[Length(min=4, max=4, message="验证码长度错误")])

    def validate_email(self, field):
        user = g.cms_user
        email = field.data
        if user.email == email:
            raise ValidationError("不能使用旧邮箱")

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # captcha_in_cache = web_cache.Memcache().get(email)
        captcha_in_cache = web_cache.RedisCache().get(email)
        if not captcha_in_cache or captcha_in_cache.lower() != captcha.lower():
            raise ValidationError("验证码错误")

