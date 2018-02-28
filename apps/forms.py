from wtforms import Form


class BaseForm(Form):
    def error_msg(self):
        return self.errors.popitem()[1][0]
