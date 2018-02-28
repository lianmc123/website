from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="邮箱格式错误"), InputRequired(message="邮箱不能为空")])
    password = StringField(validators=[Length(min=6, max=16, message="密码长度错误")])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(min=6, max=16, message="旧密码格式错误")])
    newpwd = StringField(validators=[Length(min=6, max=16, message="新密码格式错误")])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='两次输入不一致')])
