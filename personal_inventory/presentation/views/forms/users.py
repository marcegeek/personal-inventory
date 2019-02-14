import flask as fl
from flask_babel import lazy_gettext as _
from wtforms import StringField, PasswordField, SelectField, validators
from wtforms.widgets import html_params

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.views.forms import BaseForm


class LoginForm(BaseForm):
    username_email = StringField(_('Username or e-mail'),
                                 validators=[validators.DataRequired(_('Required field'))])
    password = PasswordField(_('Password'),
                             validators=[validators.DataRequired(_('Required field'))])

    def __init__(self, formdata=None):
        super().__init__(formdata=formdata)
        self.title = _('Login')
        self.submit = _('Login')
        self.fields_to_render = [self.username_email, self.password]
        self.autofocus_field = self.username_email
        self.required_msg = None
        self.extra_footer_html = '<div {}>\n'.format(html_params(class_='mt-2'))
        self.extra_footer_html += '  <a {}>'.format(html_params(href=fl.url_for('register')))
        self.extra_footer_html += _('Create account')
        self.extra_footer_html += '</a>\n'
        self.extra_footer_html += '</div>'

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
    password = PasswordField(_('Password'),
                             description=_('Field length must be between %(min)d and %(max)d',
                                           min=UserLogic.PASSWORD_LEN[0], max=UserLogic.PASSWORD_LEN[1]),
                             render_kw={'aria-describedby': 'password-description'},
                             validators=[validators.EqualTo('confirm_password', message=_('Passwords must match'))])
    confirm_password = PasswordField(_('Confirm password'))

    def __init__(self, formdata=None, languages=None, default_language=''):
        super().__init__(formdata)
        self.title = _('User registration')
        self.submit = _('Register')
        self.fields_to_render = [self.firstname, self.lastname, self.email, self.language,
                                 self.username, self.password, self.confirm_password]
        self.autofocus_field = self.firstname
        if languages is None:
            languages = {}
        self.language.choices = list(languages.items())
        if languages and default_language and not formdata:
            self.language.data = default_language
        self.firstname.mark_required = True
        self.lastname.mark_required = True
        self.email.mark_required = True
        self.username.mark_required = True
        self.language.mark_required = True
        self.password.mark_required = True
        self.confirm_password.mark_required = True

    def fill_form(self, user):
        self.title = _('User profile')
        self.submit = _('Save')
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
        user.lastname = self.lastname.data
        user.email = self.email.data
        user.username = self.username.data
        user.language = self.language.data
        if self.password.data:  # sólo se modifica si se ingresa una contraseña
            user.password = self.password.data
