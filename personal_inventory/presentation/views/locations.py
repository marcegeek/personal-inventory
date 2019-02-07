import flask as fl

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views.forms import DeleteForm
from personal_inventory.presentation.views import business_exception_handler, _retrieve_last_form, _save_last_form
from personal_inventory.presentation.views.forms.items import ItemForm
from personal_inventory.presentation.views.forms.locations import LocationForm
from personal_inventory.presentation.views.users import login_required


@login_required
def locations(user=None):
    new_location_key = 'new_location'
    forms = {new_location_key: LocationForm(fl.request.form)}

    if fl.request.method == 'GET':
        user_locations = LocationLogic().get_all_by_user(user)
        for loc in user_locations:
            # FIXME intimidad inapropiada?
            # TODO esto lo tiene que hacer la capa de negocio
            loc.items = ItemLogic().get_all_by_location(loc)

            forms['delete_location_{}'.format(loc.id)] = DeleteForm()
            item_form_key = 'new_item_in_{}'.format(loc.id)
            forms[item_form_key] = ItemForm()
            forms[item_form_key].location.choices = [(l.id, l.description) for l in user_locations]
            forms[item_form_key].location.data = str(loc.id)

        _retrieve_last_form(forms)
        return fl.render_template('locations.html', forms=forms, locations=user_locations)
    else:  # POST
        forms[new_location_key].validate()
        description = forms[new_location_key].description.data
        new_loc = Location(owner_id=user.id, description=description)

        @business_exception_handler(forms[new_location_key])
        def make_changes():
            LocationLogic().insert(new_loc)

        make_changes()
        _save_last_form(forms[new_location_key], new_location_key)
        return fl.redirect(fl.request.referrer)


@login_required
def location(location_id, user=None):
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
        current_location.items = ItemLogic().get_all_by_location(current_location)

        new_item_key = 'new_item_in_{}'.format(current_location.id)
        forms[new_item_key] = ItemForm()
        forms[new_item_key].location.choices = [
            (str(loc.id), loc.description)
            for loc in location_logic.get_all_by_user(user)
        ]
        forms[new_item_key].location.data = str(current_location.id)

        for item in current_location.items:
            edit_item_key = 'edit_item_{}'.format(item.id)
            forms[edit_item_key] = ItemForm()
            forms[edit_item_key].description.data = item.description
            forms[edit_item_key].location.choices = [
                (str(loc.id), loc.description)
                for loc in location_logic.get_all_by_user(user)
            ]
            forms[edit_item_key].location.data = str(item.location_id)
            forms[edit_item_key].quantity.data = item.quantity
            forms['delete_item_{}'.format(item.id)] = DeleteForm()

        _retrieve_last_form(forms)
        return fl.render_template('location.html', forms=forms, location=current_location)
    else:
        forms[edit_form_key].validate()
        description = forms[edit_form_key].description.data
        current_location.description = description

        @business_exception_handler(forms[edit_form_key])
        def make_changes():
            location_logic.update(current_location)

        make_changes()
        _save_last_form(forms[edit_form_key], edit_form_key)
        return fl.redirect(fl.request.referrer)


@login_required
def location_delete(location_id, user=None):
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)

    delete_form = DeleteForm(fl.request.form)
    delete_form.validate()
    @business_exception_handler(delete_form)
    def make_changes():
        location_logic.delete(location_id)

    make_changes()
    _save_last_form(delete_form, 'delete_location_{}'.format(location_id))
    return fl.redirect(fl.request.referrer)
