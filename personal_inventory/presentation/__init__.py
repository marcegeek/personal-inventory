import os

from flask import Flask, url_for, render_template, request, redirect, session, \
    flash, abort

import config
from personal_inventory.business.entities.item import Item
from personal_inventory.business.entities.location import Location
from personal_inventory.business.entities.user import User
from personal_inventory.business.logic import ValidationException
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.business.logic.user_logic import UserLogic
from personal_inventory.data import data as dal

app = Flask(__name__)

configs = config.get_configs()
dal.configure(configs['data'])
app.config.from_object(configs['flask'])
if config.ENVIRONMENT == config.Environment.DEVELOPMENT:
    os.environ['FLASK_ENV'] = 'development'
else:
    os.environ['FLASK_ENV'] = 'production'


def get_user_from_session():
    user = None
    if 'user_id' in session:
        user_id = session['user_id']
        ul = UserLogic()
        user = ul.get_by_id(user_id)
    return user


def set_user_in_session(user):
    if user is not None:
        session['user_id'] = user.id
    else:
        session.pop('user_id', None)


@app.route('/')
def home():
    user = get_user_from_session()
    return render_template('home.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']
        ul = UserLogic()
        if ul.validate_login(username_email, password):
            set_user_in_session(ul.get_by_username_email(username_email))
            return redirect(url_for('home'))
        else:
            flash('Wrong username/e-mail or password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    set_user_in_session(None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            user = User(firstname=firstname, lastname=lastname, email=email,
                        username=username, password=password)
            try:
                UserLogic().insert(user)
                set_user_in_session(user)
                return redirect(url_for('home'))
            except ValidationException as ex:
                for err in ex.args:
                    flash(str(err), 'error')
        else:
            flash('Passwords don\'t match', 'error')
    return render_template('user-editor.html', user=None)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = get_user_from_session()
    if user is not None:
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if len(password) == 0 or password == confirm_password:
                user.firstname = firstname
                user.lastname = lastname
                user.email = email
                user.username = username
                if len(password) != 0:  # si no se ingresa nada se deja sin modificar
                    user.password = password
                try:
                    UserLogic().update(user)
                    return redirect(url_for('home'))
                except ValidationException as ex:
                    for err in ex.args:
                        flash(str(err), 'error')
            else:
                flash('Passwords don\'t match', 'error')
        return render_template('user-editor.html', user=user)
    else:
        abort(401)


@app.route('/items')
def items():
    user = get_user_from_session()
    if user is not None:
        user_items = ItemLogic().get_all_by_user(user, fill_location=True)
        user_locations = LocationLogic().get_all_by_user(user)
        return render_template('items.html', items=user_items, locations=user_locations)
    return redirect(url_for('home'))


@app.route('/items/create', methods=['GET', 'POST'])
def create_item():
    user = get_user_from_session()
    if user is not None:
        if request.method == 'GET':
            user_locations = LocationLogic().get_all_by_user(user)
            if len(user_locations) == 0:
                flash('No locations were present, create one first', 'error')
                return redirect(url_for('create_location'))
            return render_template('item-editor.html', item=None,
                                   locations=user_locations)
        else:
            description = request.form['description'].strip()
            location_id = request.form['location'].strip()
            quantity = request.form['quantity'].strip()
            if len(quantity) == 0:
                quantity = None
            new_item = Item(owner_id=user.id, location_id=location_id,
                            description=description, quantity=quantity)
            try:
                ItemLogic().insert(new_item)
                return redirect(url_for('items'))
            except ValidationException as ex:
                for err in ex.args:
                    flash(str(err), 'error')
            return redirect(url_for('create_item'))
    return redirect(url_for('home'))


@app.route('/items/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    user = get_user_from_session()
    if user is not None:
        item_logic = ItemLogic()
        current_item = item_logic.get_by_id(item_id)
        if current_item is not None:
            if current_item.owner_id == user.id:
                user_locations = LocationLogic().get_all_by_user(user)
                if request.method == 'GET':
                    return render_template('item-editor.html', item=current_item, locations=user_locations)
                else:
                    description = request.form['description'].strip()
                    location_id = request.form['location'].strip()
                    quantity = request.form['quantity'].strip()
                    if len(quantity) == 0:
                        quantity = None
                    current_item.description = description
                    current_item.location_id = location_id
                    current_item.quantity = quantity
                    try:
                        item_logic.update(current_item)
                        return redirect(url_for('items'))
                    except ValidationException as ex:
                        for err in ex.args:
                            flash(str(err), 'error')
                    return redirect(url_for('item', item_id=item_id))
            else:
                abort(401)
        else:
            abort(404)
    return redirect(url_for('home'))


@app.route('/items/delete/<int:item_id>', methods=['POST'])
def item_delete(item_id):
    user = get_user_from_session()
    if user is not None:
        item_logic = ItemLogic()
        current_item = item_logic.get_by_id(item_id)
        if current_item is not None:
            if current_item.owner_id == user.id:
                confirmed = request.form.get('confirmed')
                if confirmed:
                    try:
                        item_logic.delete(item_id)
                    except ValidationException as ex:
                        for err in ex.args:
                            flash(str(err), 'error')
                return redirect(url_for('items'))
            else:
                abort(401)
        else:
            abort(404)
    return redirect(url_for('home'))


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    user = get_user_from_session()
    if user is not None:
        if request.method == 'GET':
            user_locations = LocationLogic().get_all_by_user(user)
            return render_template('locations.html', locations=user_locations)
        else:
            description = request.form['description'].strip()
            new_loc = Location(owner_id=user.id, description=description)
            try:
                LocationLogic().insert(new_loc)
            except ValidationException as ex:
                for err in ex.args:
                    flash(str(err), 'error')
            return redirect(url_for('locations'))
    return redirect(url_for('home'))


@app.route('/locations/<int:location_id>', methods=['GET', 'POST'])
def location(location_id):
    user = get_user_from_session()
    if user is not None:
        location_logic = LocationLogic()
        current_location = location_logic.get_by_id(location_id)
        if current_location is not None:
            if current_location.owner_id == user.id:
                if request.method == 'GET':
                    return render_template('location.html',
                                           location=current_location)
                else:
                    delete = request.form.get('delete')
                    if not delete:
                        description = request.form['description'].strip()
                        current_location.description = description
                        try:
                            location_logic.update(current_location)
                            return redirect(request.referrer)
                        except ValidationException as ex:
                            for err in ex.args:
                                flash(str(err), 'error')
                        return redirect(request.referrer)
                    else:
                        location_logic.delete(location_id)
                        return redirect(request.referrer)
            else:
                abort(401)
        else:
            abort(404)
    return redirect(url_for('home'))
