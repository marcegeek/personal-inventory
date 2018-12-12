from wtforms import StringField, PasswordField, validators, SelectField

from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.forms import BaseForm


class UserEditForm(BaseForm):
    firstname = StringField('First name', description='Must be between {} and {}'.format(*UserLogic.NAME_LEN),
                            render_kw={'aria-describedby': 'firstname-description'})
    lastname = StringField('Last name', description='Must be between {} and {}'.format(*UserLogic.NAME_LEN),
                           render_kw={'aria-describedby': 'firstname-description'})
    email = StringField('E-mail', description='Must be between {} and {}'.format(*UserLogic.EMAIL_LEN),
                        render_kw={'aria-describedby': 'firstname-description'})
    username = StringField('Username')
    language = SelectField("Language")
    password = PasswordField('New password', validators=[validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password')
