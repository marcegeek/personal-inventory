from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, validators, SelectField

from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.views.forms import BaseForm


class LoginForm(BaseForm):
    username_email = StringField(_('Username or e-mail'))
    password = PasswordField(_('Password'))


class UserEditForm(BaseForm):
    firstname = StringField(_('First name'),
                            description=_('Field length must be between %(min)d and %(max)d', min=UserLogic.NAME_LEN[0],
                                          max=UserLogic.NAME_LEN[1]),
                            render_kw={'aria-describedby': 'firstname-description'})
    lastname = StringField(_('Last name'),
                           description=_('Field length must be between %(min)d and %(max)d', min=UserLogic.NAME_LEN[0],
                                         max=UserLogic.NAME_LEN[1]),
                           render_kw={'aria-describedby': 'lastname-description'})
    email = StringField(_('E-mail'),
                        description=_('Field length must be between %(min)d and %(max)d', min=UserLogic.EMAIL_LEN[0],
                                      max=UserLogic.EMAIL_LEN[1]),
                        render_kw={'aria-describedby': 'email-description'})
    username = StringField(_('Username'))
    language = SelectField(_('Language'))
    password = PasswordField(_('New password'),
                             validators=[validators.EqualTo('confirm_password', message=_('Passwords must match'))])
    confirm_password = PasswordField(_('Confirm password'))
