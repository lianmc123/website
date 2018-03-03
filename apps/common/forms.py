from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import Regexp, InputRequired
import config


class SMSCaptchaForm(BaseForm):
    salt = config.SMS_SALT
    telephone = StringField(validators=[Regexp(r'1[34579]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data