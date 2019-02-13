from flask_babel import lazy_gettext as _
from wtforms import StringField

from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views.forms import BaseForm


class LocationForm(BaseForm):
    description = StringField(_('Description'),
                              description=_('Field length must be between %(min)d and %(max)d',
                                            min=LocationLogic.DESCRIPTION_LEN[0], max=LocationLogic.DESCRIPTION_LEN[1]),
                              render_kw={'aria-describedby': 'description-description'})

    def __init__(self, formdata=None):
        super().__init__(formdata=formdata)
        self.description.mark_required = True

    def fill_form(self, location):
        self.description.data = location.description

    def make_object(self, **kwargs):
        return Location(owner_id=kwargs.get('owner_id', None),
                        description=self.description.data)

    def update_object(self, location):
        location.description = self.description.data
