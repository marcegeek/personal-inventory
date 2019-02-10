from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, SelectField, validators

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.views.forms import BaseForm


class LoginForm(BaseForm):
    username_email = StringField(_('Username or e-mail'))
    password = PasswordField(_('Password'))

    def fill_form(self, obj, **kwargs):
        pass

    def make_object(self):
        pass

    def update_object(self, obj):
        pass


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
                        description=_('Field must be a valid e-mail adress and its length must be between %(min)d and %(max)d',
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

    def __init__(self, formdata=None, languages=None, default_language=''):
        super().__init__(formdata)
        if languages is None:
            languages = {}
        self.language.choices = list(languages.items())
        if languages and default_language:
            self.language.data = default_language

    def fill_form(self, user):
        self.firstname.data = user.firstname
        self.lastname.data = user.lastname
        self.email.data = user.email
        self.username.data = user.username
        self.language.data = user.language
        # la contraseña no se rellena, además si se implementa cifrado
        # de hecho sería imposible mostrarla

    def make_object(self, **kwargs):
        return User(firstname=self.firstname.data, lastname=self.lastname.data, email=self.email.data,
                    username=self.username.data, language=self.language.data, password=self.password.data)

    def update_object(self, user):
        user.firstname = self.firstname.data
        user.lastname = self.username.data
        user.email = self.email.data
        user.username = self.username.data
        user.language = self.language.data
        if self.password.data:  # sólo se modifica si se ingresa una contraseña
            user.password = self.password.data
