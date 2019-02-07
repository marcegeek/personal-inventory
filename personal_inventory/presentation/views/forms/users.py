from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, SelectField, validators

from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.views.forms import BaseForm


class LoginForm(BaseForm):
    username_email = StringField(_('Username or e-mail'))
    password = PasswordField(_('Password'))


class UserEditForm(BaseForm):
    firstname = StringField(_('First name'),
                            description=_('Field length must be between %(min)d and %(max)d',
                                          min=UserLogic.NAME_LEN[0], max=UserLogic.NAME_LEN[1]),
                            render_kw={'aria-describedby': 'firstname-description'})
    lastname = StringField(_('Last name'),
                           description=_('Field length must be between %(min)d and %(max)d',
                                         min=UserLogic.NAME_LEN[0], max=UserLogic.NAME_LEN[1]),
                           render_kw={'aria-describedby': 'lastname-description'})
    email = StringField(_('E-mail'),
                        udescription=_('Field must be a valid e-mail adress and its length must be between %(min)d and %(max)d',
                                      min=UserLogic.EMAIL_LEN[0], max=UserLogic.EMAIL_LEN[1]),
                        render_kw={'aria-describedby': 'email-description'})
    username = StringField(_('Username'),
                           description=_('Field must be made of lowercase letters, digits and underscores and its length must be between %(min)d and %(max)d',
                                         min=UserLogic.USERNAME_LEN[0], max=UserLogic.USERNAME_LEN[1]),
                           render_kw={'aria-describedby': 'username-description'})
    language = SelectField(_('Language'))
    password = PasswordField(_('New password'),
                             description=_('Field length must be between %(min)d and %(max)d',
                                           min=UserLogic.PASSWORD_LEN[0], max=UserLogic.PASSWORD_LEN[1]),
                             render_kw={'aria-describedby': 'password-description'},
                             validators=[validators.EqualTo('confirm_password', message=_('Passwords must match'))])
    confirm_password = PasswordField(_('Confirm password'))
