from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length


class LoginForm(Form):
    email = StringField(validators=[Email(message="邮箱格式错误"), InputRequired(message="邮箱不能为空")])
    password = StringField(validators=[Length(min=6, max=16, message="密码长度错误")])
    remember = IntegerField()