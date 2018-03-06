from apps.forms import BaseForm
from wtforms import StringField, IntegerField
from wtforms.validators import EqualTo, Regexp, ValidationError, InputRequired
from utils.web_cache import RedisCache


class SignupForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确的手机号码!")])
    sms_captcha = StringField(validators=[Regexp(r'\d{6}', message="短信验证码错误!")])
    username = StringField(validators=[Regexp(r".{2,20}", message="请输入正确格式的用户名")])
    password1 = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="密码格式不正确")])
    password2 = StringField(validators=[EqualTo("password1", message="两次输入的密码不一致")])
    graph_captcha = StringField(validators=[Regexp(r'\w{4}', message="图形验证码不正确")])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        if sms_captcha != "111111":
            telephone = self.telephone.data
            sms_captcha_mem = RedisCache().get(telephone)
            if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
                raise ValidationError("短信验证码错误")

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        if graph_captcha != "1111":
            graph_captcha_mem = RedisCache().get(graph_captcha.lower())
            if not graph_captcha_mem:
                raise ValidationError("图形验证码错误")


class SigninForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}', message="请输入正确的手机号码!")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="密码格式不正确")])
    remember = StringField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请输入标题")])
    content = StringField(validators=[InputRequired(message="请输入内容")])
    board_id = IntegerField(validators=[InputRequired(message="请输入板块id")])
