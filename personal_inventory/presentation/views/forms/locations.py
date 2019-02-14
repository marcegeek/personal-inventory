import flask as fl
from flask_babel import lazy_gettext as _
from wtforms import StringField

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views.forms import BaseForm, DeleteForm


class LocationForm(BaseForm):
    """Formulario de edición de ubicación"""

    description = StringField(_('Description'),
                              description=_('Field length must be between %(min)d and %(max)d',
                                            min=LocationLogic.DESCRIPTION_LEN[0], max=LocationLogic.DESCRIPTION_LEN[1]),
                              render_kw={'aria-describedby': 'description-description'})

    def __init__(self, formdata=None):
        super().__init__(formdata=formdata)
        self.title = _('New location')
        self.modal_id = 'new-location-modal'
        self.action = fl.url_for('locations')
        self.fields_to_render = [self.description]
        self.autofocus_field = self.description
        self.description.mark_required = True

    def fill(self, location):
        self.title = _('Editing location')
        self.modal_id = 'edit-location-{}-modal'.format(location.id)
        self.action = fl.url_for('location', location_id=location.id)
        self.description.data = location.description

    def make_object(self, **kwargs):
        return Location(owner_id=kwargs.get('owner_id', None),
                        description=self.description.data)

    def update_object(self, location):
        location.description = self.description.data


class LocationDeleteForm(DeleteForm):
    """Formulario de eliminación de ubicación"""

    def __init__(self, formdata=None, location=None):
        super().__init__(formdata=formdata)
        if location is not None:
            self.title = _('Delete location')
            self.modal_id = 'delete-location-{}-modal'.format(location.id)
            self.action = fl.url_for('location_delete', location_id=location.id)
            self.extra_body_html = self.delete_body(location.description)
