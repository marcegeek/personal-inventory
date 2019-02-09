import os

import flask as fl
import flask_babel

import config
import personal_inventory.data as dal
from personal_inventory.presentation.views import users as user_views
from personal_inventory.presentation.views import locations as location_views
from personal_inventory.presentation.views import items as item_views

app = fl.Flask(__name__)

configs = config.get_configs()
dal.configure(configs['data'])
app.config.from_object(configs['flask'])
if config.ENVIRONMENT == config.Environment.DEVELOPMENT:
    os.environ['FLASK_ENV'] = 'development'
else:
    os.environ['FLASK_ENV'] = 'production'

babel = flask_babel.Babel(app)


@babel.localeselector
def get_language():
    # si hay un usuario logueado, tomar la localización
    # de la configuración del usuario
    user = user_views.get_logged_in_user()
    if user and user.language:
        return user.language
    # si no, tomarla de la request que envía el navegador
    return fl.request.accept_languages.best_match(config.LANGUAGES.keys())


@app.route('/')
def home():
    user = user_views.get_logged_in_user()
    return fl.render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return user_views.login()


@app.route('/logout')
def logout():
    return user_views.logout()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return user_views.register(config.LANGUAGES, get_language())


@app.route('/profile', methods=['GET', 'POST'])
def edit_profile():
    return user_views.profile(config.LANGUAGES)


@app.route('/items', methods=['GET', 'POST'])
def items():
    return item_views.items()


@app.route('/items/<int:item_id>', methods=['POST'])
def item(item_id):
    return item_views.item(item_id)


@app.route('/items/<int:item_id>/delete', methods=['POST'])
def item_delete(item_id):
    return item_views.item_delete(item_id)


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    return location_views.locations()


@app.route('/locations/<int:location_id>', methods=['GET', 'POST'])
def location(location_id):
    return location_views.location(location_id)


@app.route('/locations/<int:location_id>/delete', methods=['POST'])
def location_delete(location_id):
    return location_views.location_delete(location_id)


@app.errorhandler(404)
def page_not_found(e):
    return fl.render_template('404.html'), 404


@app.errorhandler(401)
def unauthorized_resource(e):
    return fl.render_template('401.html'), 401


@app.errorhandler(405)
def method_not_allowed(e):
    return fl.render_template('405.html'), 405
