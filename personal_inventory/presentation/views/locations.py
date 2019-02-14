import flask as fl

from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views.forms import DeleteForm
from personal_inventory.presentation.views import business_exception_handler, _retrieve_last_form, _save_last_form
from personal_inventory.presentation.views.forms.items import ItemForm, ItemDeleteForm
from personal_inventory.presentation.views.forms.locations import LocationForm, LocationDeleteForm
from personal_inventory.presentation.views.users import login_required


@login_required
def locations(user=None):
    new_location_key = 'new_location'
    forms = {new_location_key: LocationForm(fl.request.form)}

    if fl.request.method == 'GET':
        user_locations = LocationLogic().get_all_by_user(user, populate_items=True)
        for loc in user_locations:
            edit_form_key = 'edit_location_{}'.format(loc.id)
            forms[edit_form_key] = LocationForm()
            forms[edit_form_key].fill(loc)
            forms['delete_location_{}'.format(loc.id)] = LocationDeleteForm(location=loc)
            item_form_key = 'new_item_in_{}'.format(loc.id)
            forms[item_form_key] = ItemForm(locations=user_locations, default_location=loc)

        _retrieve_last_form(forms)
        return fl.render_template('locations.html', forms=forms, locations=user_locations)
    else:  # POST
        if forms[new_location_key].validate():
            new_loc = forms[new_location_key].make_object(owner_id=user.id)

            @business_exception_handler(forms[new_location_key])
            def make_changes():
                LocationLogic().insert(new_loc)

            make_changes()
        _save_last_form(forms[new_location_key], new_location_key)
        return fl.redirect(fl.request.referrer)


@login_required
def location(location_id, user=None):
    location_logic = LocationLogic()
    current_location = location_logic.get_by_id(location_id, populate_items=True)
    if current_location is None:
        fl.abort(404)
    if current_location.owner_id != user.id:
        fl.abort(401)
    edit_form_key = 'edit_location_{}'.format(location_id)
    delete_form_key = 'delete_location_{}'.format(location_id)
    forms = {
        edit_form_key: LocationForm(fl.request.form),
        delete_form_key: LocationDeleteForm(location=current_location)
    }

    if fl.request.method == 'GET':
        user_locations = location_logic.get_all_by_user(user)
        forms[edit_form_key].fill(current_location)

        new_item_key = 'new_item_in_{}'.format(current_location.id)
        forms[new_item_key] = ItemForm(locations=user_locations, default_location=current_location)

        for item in current_location.items:
            edit_item_key = 'edit_item_{}'.format(item.id)
            forms[edit_item_key] = ItemForm(locations=user_locations)
            forms[edit_item_key].fill(item)
            forms['delete_item_{}'.format(item.id)] = ItemDeleteForm(item=item)

        _retrieve_last_form(forms)
        return fl.render_template('location.html', forms=forms, location=current_location)
    else:  # POST
        if forms[edit_form_key].validate():
            forms[edit_form_key].update_object(current_location)

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
    redir = None
    if delete_form.validate():

        @business_exception_handler(delete_form)
        def make_changes():
            location_logic.delete(location_id)
            # si se elimina la ubicación desde su propia vista,
            # ya no tiene sentido volver a la misma, hay que ir al
            # listado de ubicaciones
            return fl.redirect(fl.url_for('locations'))

        redir = make_changes()
    _save_last_form(delete_form, 'delete_location_{}'.format(location_id))
    if redir:
        return redir
    return fl.redirect(fl.request.referrer)
