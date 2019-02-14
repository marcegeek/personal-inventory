import functools

import flask as fl
from flask_babel import gettext as _

import config
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
            fl.flash(_('Wrong username/e-mail or password'), 'error')
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


def register():
    from personal_inventory.presentation import get_language
    form = UserEditForm(fl.request.form, languages=config.LANGUAGES, default_language=get_language())

    if fl.request.method == 'POST' and form.validate():
        user = form.make_object()

        @business_exception_handler(form)
        def make_changes():
            UserLogic().insert(user)
            return fl.redirect(fl.url_for('login'))

        redir = make_changes()
        if redir:
            return redir
    return fl.render_template('user-profile.html', form=form)


@login_required
def profile(user=None):
    form = UserEditForm(fl.request.form, languages=config.LANGUAGES)
    form.password.description = _('Leave it blank to keep the current password')
    form.password.mark_required = False
    form.confirm_password.mark_required = False

    if fl.request.method == 'GET':
        form.fill_form(user)
    elif fl.request.method == 'POST' and form.validate():
        form.update_object(user)

        @business_exception_handler(form)
        def make_changes():
            UserLogic().update(user)
            return fl.redirect(fl.url_for('home'))

        redir = make_changes()
        if redir:
            return redir
    return fl.render_template('user-profile.html', user=user, form=form)
