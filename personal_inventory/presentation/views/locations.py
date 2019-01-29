import flask as fl

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views import business_exception_handler
from personal_inventory.presentation.forms.locations import LocationForm


def locations(user):
    if user is None:
        fl.flash('Please login to use the application', category='info')
        return fl.redirect(fl.url_for('login'))
    location_form = LocationForm(fl.request.form)
    if 'errors' in fl.session:
        errors = fl.session.pop('errors')
        location_form.errors = errors
        if 'form_data' in fl.session:
            form_data = fl.session.pop('form_data')
    if fl.request.method == 'POST' and location_form.validate():
        description = location_form.description.data
        new_loc = Location(owner_id=user.id, description=description)

        @business_exception_handler(location_form)
        def make_changes():
            LocationLogic().insert(new_loc)

        make_changes()
        fl.session['errors'] = location_form.errors
        if location_form.errors:
            fl.session['form_data'] = location_form.data
        return fl.redirect(fl.request.referrer)
    user_locations = LocationLogic().get_all_by_user(user)
    for loc in user_locations:
        # FIXME intimidad inapropiada?
        # TODO esto lo tiene que hacer la capa de negocio
        loc.items = ItemLogic().get_all_by_location(loc)
    if location_form.field_errors:
        for field in location_form.field_errors:
            if field in form_data:
                location_form[field].data = form_data[field]
    return fl.render_template('locations.html', location_form=location_form, locations=user_locations)


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
    if 'errors' in fl.session:
        errors = fl.session.pop('errors')
        edit_form.errors = errors
        if 'form_data' in fl.session:
            form_data = fl.session.pop('form_data')
    if fl.request.method == 'GET':
        edit_form.description.data = current_location.description
        all_locations = location_logic.get_all_by_user(user)
        current_location.items = ItemLogic().get_all_by_location(current_location)
        if edit_form.field_errors:
            for field in edit_form.field_errors:
                if field in form_data:
                    edit_form[field].data = form_data[field]
        return fl.render_template('location.html', form=edit_form,
                                  location=current_location, locations=all_locations)
    elif edit_form.validate():
        delete = fl.request.form.get('delete')  # arreglar esto
        if not delete:
            description = edit_form.description.data
            current_location.description = description

            @business_exception_handler(edit_form)
            def make_changes():
                location_logic.update(current_location)

            make_changes()
            fl.session['errors'] = edit_form.errors
            if edit_form.errors:
                fl.session['form_data'] = edit_form.data
            return fl.redirect(fl.request.referrer)
        else:
            @business_exception_handler(edit_form)
            def make_changes():
                location_logic.delete(location_id)

            make_changes()
            fl.session['errors'] = edit_form.errors
            return fl.redirect(fl.request.referrer)
