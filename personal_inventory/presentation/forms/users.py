from wtforms import StringField, PasswordField, validators, SelectField

from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.forms import BaseForm


class UserEditForm(BaseForm):
    firstname = StringField('First name', validators=[validators.DataRequired(),
                                                      validators.Length(*UserLogic.NAME_LEN)],
                            description='Must be between {} and {}'.format(*UserLogic.NAME_LEN),
                            render_kw={'aria-describedby': 'firstname-description'})
    lastname = StringField('Last name', validators=[validators.DataRequired(), validators.Length(*UserLogic.NAME_LEN)],
                           description='Must be between {} and {}'.format(*UserLogic.NAME_LEN),
                           render_kw={'aria-describedby': 'firstname-description'})
    email = StringField('E-mail', validators=[validators.DataRequired(),
                                              validators.Length(*UserLogic.EMAIL_LEN)],
                        description='Must be between {} and {}'.format(*UserLogic.EMAIL_LEN),
                        render_kw={'aria-describedby': 'firstname-description'})
    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(*UserLogic.USERNAME_LEN),
                                                   validators.Regexp('[a-z0-9_]+', message='El nombre de usuario debe estar formado por letras minúsculas, dígitos y guiones bajos')])
    language = SelectField("Language", validators=[
        validators.DataRequired()
    ])
    password = PasswordField('New password', [
        validators.DataRequired(),
        validators.Length(*UserLogic.PASSWORD_LEN),
        validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password')
