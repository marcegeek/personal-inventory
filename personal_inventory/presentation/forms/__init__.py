from wtforms import Form, StringField, PasswordField, SelectField, validators


class BaseForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_errors = []
