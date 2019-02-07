import functools

import flask as fl
from flask_babel import gettext as _

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation.views import business_exception_handler
from personal_inventory.presentation.views.forms.users import UserEditForm, LoginForm


def get_logged_in_user():
    user = None
    if 'user_id' in fl.session:
        user_id = fl.session['user_id']
        ul = UserLogic()
        user = ul.get_by_id(user_id)
    return user


def set_logged_in_user(user):
    if user is not None:
        fl.session['user_id'] = user.id
    else:
        fl.session.pop('user_id', None)


def login():
    form = LoginForm(fl.request.form)
    if fl.request.method == 'POST' and form.validate():
        username_email = form.username_email.data
        password = form.password.data
        ul = UserLogic()
        if ul.validate_login(username_email, password):
            set_logged_in_user(ul.get_by_username_email(username_email))
            redir = fl.session.pop('redirect', fl.url_for('home'))
            return fl.redirect(redir)
        else:
            form.global_errors.append(_('Wrong username/e-mail or password'))
    return fl.render_template('login.html', form=form)


def logout():
    set_logged_in_user(None)
    return fl.redirect(fl.url_for('home'))


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user = get_logged_in_user()
        if user is None:
            fl.flash(_('Please login to use the application'), category='info')
            fl.session['redirect'] = fl.request.url
            return fl.redirect(fl.url_for('login'))
        return func(user=user, *args, **kwargs)

    return wrapper


def register(languages, default_language):
    form = UserEditForm(fl.request.form)
    form.language.choices = [(key, languages[key]) for key in languages]
    form.language.data = default_language
    if fl.request.method == 'POST':
        form.validate()
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        language = form.language.data
        user = User(firstname=firstname, lastname=lastname, email=email,
                    username=username, password=password, language=language)

        @business_exception_handler(form)
        def make_changes():
            UserLogic().insert(user)
            return fl.redirect(fl.url_for('login'))

        redir = make_changes()
        if redir:
            return redir
    return fl.render_template('user-editor.html', form=form)


@login_required
def profile(languages, user=None):
    form = UserEditForm(fl.request.form)
    form.password.description = _('Leave it blank to keep the current password')
    form.language.choices = [(key, languages[key]) for key in languages]

    if fl.request.method == 'GET':
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.email.data = user.email
        form.language.data = user.language
        form.username.data = user.username
    elif fl.request.method == 'POST':
        form.validate()
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        language = form.language.data

        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.username = username
        user.language = language
        if len(password) != 0:  # si no se ingresa nada se deja sin modificar
            user.password = password

        @business_exception_handler(form)
        def make_changes():
            UserLogic().update(user)
            return fl.redirect(fl.url_for('home'))

        redir = make_changes()
        if redir:
            return redir
    return fl.render_template('user-editor.html', user=user, form=form)
