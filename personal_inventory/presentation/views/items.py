import flask as fl
from flask_babel import gettext as _

from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views import _retrieve_last_form, business_exception_handler, _save_last_form
from personal_inventory.presentation.views.forms import DeleteForm
from personal_inventory.presentation.views.forms.items import ItemForm
from personal_inventory.presentation.views.users import login_required


@login_required
def items(user=None):
    user_locations = LocationLogic().get_all_by_user(user)
    user_locations.sort(key=lambda l: l.description)
    user_locations_dic = dict([(l.id, l.description) for l in user_locations])

    new_item_key = 'new_item'
    forms = {new_item_key: ItemForm(fl.request.form, locations=user_locations)}

    if fl.request.method == 'GET':
        if len(user_locations) == 0:
            fl.flash(_('No locations yet, create one first'), 'error')
            return fl.redirect(fl.url_for('locations'))
        user_items = ItemLogic().get_all_by_user(user, fill_location=True)
        user_items.sort(key=lambda i: (user_locations_dic[i.location_id], i.description))

        for it in user_items:
            edit_form_key = 'edit_item_{}'.format(it.id)
            delete_form_key = 'delete_item_{}'.format(it.id)
            forms[edit_form_key] = ItemForm(locations=user_locations)
            forms[edit_form_key].fill_form(it)
            forms[delete_form_key] = DeleteForm()

        _retrieve_last_form(forms)
        return fl.render_template('items.html', forms=forms, items=user_items, locations=user_locations)
    else:  # POST
        if forms[new_item_key].validate():
            new_item = forms[new_item_key].make_object(owner_id=user.id)

            @business_exception_handler(forms[new_item_key])
            def make_changes():
                ItemLogic().insert(new_item)

            make_changes()
        # si estoy creando el ítem desde una ubicación/listado de ubicaciones
        if 'location' in fl.request.referrer:
            form = forms.pop(new_item_key)
            new_item_key = 'new_item_in_{}'.format(form.location.data)
            forms[new_item_key] = form
        _save_last_form(forms[new_item_key], new_item_key)
        return fl.redirect(fl.request.referrer)


@login_required
def item(item_id, user=None):
    item_logic = ItemLogic()
    current_item = item_logic.get_by_id(item_id)
    if current_item is None:
        fl.abort(404)
    if current_item.owner_id != user.id:
        fl.abort(401)

    edit_form = ItemForm(fl.request.form,
                         locations=LocationLogic().get_all_by_user(user))
    if edit_form.validate():
        edit_form.update_object(current_item)

        @business_exception_handler(edit_form)
        def make_changes():
            item_logic.update(current_item)

        make_changes()
    _save_last_form(edit_form, 'edit_item_{}'.format(item_id))
    return fl.redirect(fl.request.referrer)


@login_required
def item_delete(item_id, user=None):
    item_logic = ItemLogic()
    current_item = item_logic.get_by_id(item_id)
    if current_item is None:
        fl.abort(404)
    if current_item.owner_id != user.id:
        fl.abort(401)

    delete_form = DeleteForm(fl.request.form)
    if delete_form.validate():

        @business_exception_handler(delete_form)
        def make_changes():
            item_logic.delete(item_id)

        make_changes()
    _save_last_form(delete_form, 'delete_item_{}'.format(item_id))
    return fl.redirect(fl.request.referrer)
