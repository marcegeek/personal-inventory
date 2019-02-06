import flask as fl

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.forms import BaseForm
from personal_inventory.presentation.views import business_exception_handler
from personal_inventory.presentation.forms.locations import LocationForm


def locations(user):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    forms = {'new_location': LocationForm(fl.request.form)}

    if fl.request.method == 'GET':
        last_form = None
        new_location_form_data = {}
        if 'last_form' in fl.session:
            last_form = fl.session.pop('last_form')
            if last_form['id'] == 'new_location':
                forms['new_location'].errors = last_form['errors']
                new_location_form_data = last_form['data']
        user_locations = LocationLogic().get_all_by_user(user)
        for loc in user_locations:
            # FIXME intimidad inapropiada?
            # TODO esto lo tiene que hacer la capa de negocio
            loc.items = ItemLogic().get_all_by_location(loc)
            forms['delete_location_{}'.format(loc.id)] = BaseForm()
            if last_form and last_form['id'] == 'delete_location_{}'.format(loc.id):
                forms['delete_location_{}'.format(loc.id)].errors = last_form['errors']
        if forms['new_location'].field_errors:
            for field in new_location_form_data:
                forms['new_location'][field].data = new_location_form_data[field]
        return fl.render_template('locations.html', forms=forms, locations=user_locations)
    elif forms['new_location'].validate():  # POST
        description = forms['new_location'].description.data
        new_loc = Location(owner_id=user.id, description=description)

        @business_exception_handler(forms['new_location'])
        def make_changes():
            LocationLogic().insert(new_loc)

        make_changes()
        fl.session['last_form'] = {'id': 'new_location',
                                   'errors': forms['new_location'].errors,
                                   'data': forms['new_location'].data}
        return fl.redirect(fl.request.referrer)


def location(user, location_id):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id)
    edit_form = LocationForm(fl.request.form)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)
    last_form = None
    form_data = {}
    if 'last_form' in fl.session:
        last_form = fl.session.pop('last_form')
        if last_form['id'] == 'edit_location_{}'.format(location_id):
            edit_form.errors = last_form['errors']
            form_data = last_form['data']
    if fl.request.method == 'GET':
        edit_form.description.data = current_location.description
        all_locations = location_logic.get_all_by_user(user)
        current_location.items = ItemLogic().get_all_by_location(current_location)
        if edit_form.field_errors:
            for field in form_data:
                edit_form[field].data = form_data[field]
        return fl.render_template('location.html', form=edit_form,
                                  location=current_location, locations=all_locations)
    elif edit_form.validate():
        description = edit_form.description.data
        current_location.description = description

        @business_exception_handler(edit_form)
        def make_changes():
            location_logic.update(current_location)

        make_changes()
        fl.session['last_form'] = {'id': 'edit_location_{}'.format(location_id),
                                   'errors': edit_form.errors,
                                   'data': edit_form.data}
        return fl.redirect(fl.request.referrer)


def location_delete(user, location_id):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id)
    delete_form = BaseForm(fl.request.form)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)
    if 'last_form' in fl.session:
        fl.session.pop('last_form')
    if delete_form.validate():
        @business_exception_handler(delete_form)
        def make_changes():
            location_logic.delete(location_id)

        make_changes()
        fl.session['last_form'] = {'id': 'delete_location_{}'.format(location_id),
                                   'errors': delete_form.errors}
    return fl.redirect(fl.request.referrer)
