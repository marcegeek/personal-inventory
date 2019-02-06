import flask as fl

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.forms import DeleteForm
from personal_inventory.presentation.views import business_exception_handler, _retrieve_last_form, _save_last_form
from personal_inventory.presentation.forms.locations import LocationForm


def locations(user):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    new_location_key = 'new_location'
    forms = {new_location_key: LocationForm(fl.request.form)}

    if fl.request.method == 'GET':
        user_locations = LocationLogic().get_all_by_user(user)
        for loc in user_locations:
            # FIXME intimidad inapropiada?
            # TODO esto lo tiene que hacer la capa de negocio
            loc.items = ItemLogic().get_all_by_location(loc)

            delete_location_key = 'delete_location_{}'.format(loc.id)
            forms[delete_location_key] = DeleteForm()

        _retrieve_last_form(forms)
        return fl.render_template('locations.html', forms=forms, locations=user_locations)
    elif forms[new_location_key].validate():  # POST
        description = forms[new_location_key].description.data
        new_loc = Location(owner_id=user.id, description=description)

        @business_exception_handler(forms[new_location_key])
        def make_changes():
            LocationLogic().insert(new_loc)

        make_changes()
        _save_last_form(forms[new_location_key], new_location_key)
        return fl.redirect(fl.request.referrer)


def location(user, location_id):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)
    edit_form_key = 'edit_location_{}'.format(location_id)
    delete_form_key = 'delete_location_{}'.format(location_id)
    forms = {
        edit_form_key: LocationForm(fl.request.form),
        delete_form_key: DeleteForm()
    }

    if fl.request.method == 'GET':
        forms[edit_form_key].description.data = current_location.description
        all_locations = location_logic.get_all_by_user(user)
        current_location.items = ItemLogic().get_all_by_location(current_location)
        _retrieve_last_form(forms)
        return fl.render_template('location.html', forms=forms,
                                  location=current_location, locations=all_locations)
    elif forms[edit_form_key].validate():
        description = forms[edit_form_key].description.data
        current_location.description = description

        @business_exception_handler(forms[edit_form_key])
        def make_changes():
            location_logic.update(current_location)

        make_changes()
        _save_last_form(forms[edit_form_key], edit_form_key)
        return fl.redirect(fl.request.referrer)


def location_delete(user, location_id):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)
    delete_form_key = 'delete_location_{}'.format(location_id)
    delete_form = DeleteForm(fl.request.form)
    if delete_form.validate():
        @business_exception_handler(delete_form)
        def make_changes():
            location_logic.delete(location_id)

        make_changes()
        _save_last_form(delete_form, delete_form_key)
    return fl.redirect(fl.request.referrer)
