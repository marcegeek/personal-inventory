import os

from flask import Flask, url_for, render_template, request, redirect, session, \
    flash, abort
import flask_babel as fl_babel

import config
from personal_inventory.presentation.views import users as user_views
from personal_inventory.presentation.views import locations as location_views
from personal_inventory.presentation.views import items as item_views
from personal_inventory.business.entities.item import Item
from personal_inventory.business.logic import ValidationException
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.data import data as dal
from personal_inventory.presentation import error_handler

app = Flask(__name__)

configs = config.get_configs()
dal.configure(configs['data'])
app.config.from_object(configs['flask'])
if config.ENVIRONMENT == config.Environment.DEVELOPMENT:
    os.environ['FLASK_ENV'] = 'development'
else:
    os.environ['FLASK_ENV'] = 'production'

babel = fl_babel.Babel(app)


def get_logged_in_user():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        ul = UserLogic()
        user = ul.get_by_id(user_id)
    return user


def set_logged_in_user(user):
    if user is not None:
        session['user_id'] = user.id
    else:
        session.pop('user_id', None)


@babel.localeselector
def get_language():
    # si hay un usuario logueado, tomar la localización
    # de la configuración del usuario
    user = get_logged_in_user()
    if user and user.language:
        return user.language
    # si no, tomarla de la request que envía el navegador
    return request.accept_languages.best_match(config.LANGUAGES.keys())


@app.route('/')
def home():
    user = get_logged_in_user()
    return render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']
        ul = UserLogic()
        if ul.validate_login(username_email, password):
            set_logged_in_user(ul.get_by_username_email(username_email))
            return redirect(url_for('home'))
        else:
            flash(fl_babel.gettext('Wrong username/e-mail or password'), 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    set_logged_in_user(None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    return user_views.register(config.LANGUAGES, get_language())


@app.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    return user_views.profile(get_logged_in_user(), config.LANGUAGES)


@app.route('/items', methods=['GET', 'POST'])
def items():
    return item_views.items(get_logged_in_user())


@app.route('/items/<int:item_id>', methods=['POST'])
def item(item_id):
    return item_views.item(get_logged_in_user(), item_id)


@app.route('/items/<int:item_id>/delete', methods=['POST'])
def item_delete(item_id):
    return item_views.item_delete(get_logged_in_user(), item_id)


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    return location_views.locations(get_logged_in_user())


@app.route('/locations/<int:location_id>', methods=['GET', 'POST'])
def location(location_id):
    return location_views.location(get_logged_in_user(), location_id)


@app.route('/locations/<int:location_id>/delete', methods=['POST'])
def location_delete(location_id):
    return location_views.location_delete(get_logged_in_user(), location_id)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def unauthorized_resource(e):
    return render_template('401.html'), 401


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405
