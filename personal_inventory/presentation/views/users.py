import flask as fl

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic import ValidationException
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.presentation import error_handler
from personal_inventory.presentation.views import business_exception_handler
from personal_inventory.presentation.forms.users import UserEditForm


def register(languages, default_language):
    form = UserEditForm(fl.request.form)
    form.language.choices = [(key, languages[key]) for key in languages]
    form.language.data = default_language
    if fl.request.method == 'POST' and form.validate():
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


def profile(user, languages):
    if user is not None:
        form = UserEditForm(fl.request.form)
        form.password.description = 'Leave it blank to keep the current password'
        form.language.choices = [(key, languages[key]) for key in languages]

        if fl.request.method == 'GET':
            form.firstname.data = user.firstname
            form.lastname.data = user.lastname
            form.email.data = user.email
            form.language.data = user.language
            form.username.data = user.username
        elif fl.request.method == 'POST' and form.validate():
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
    else:
        fl.abort(401)
