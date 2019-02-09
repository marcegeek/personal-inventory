from flask_babel import lazy_gettext as _
from wtforms import StringField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms import validators

from personal_inventory.business.entities.item import Item
from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.presentation.views.forms import BaseForm


class ItemForm(BaseForm):
    description = StringField(_('Description'), description=_('Field length must be between %(min)d and %(max)d', min=ItemLogic.DESCRIPTION_LEN[0], max=ItemLogic.DESCRIPTION_LEN[1]),
                              render_kw={'aria-describedby': 'description-description'})
    location = SelectField(_('Location'), coerce=int)
    quantity = IntegerField(_('Quantity'), description=_('Optional field, must be a non-negative integer number'),
                            render_kw={'aria-describedby': 'quantity-description'},
                            validators=[validators.Optional()])

    def ensure_form_ready(self, **kwargs):
        locations = kwargs.get('locations', [])
        self.location.choices = [(loc.id, loc.description)
                                 for loc in locations]

    def fill_form(self, item, **kwargs):
        self.ensure_form_ready(**kwargs)
        self.description.data = item.description
        self.location.data = item.location_id
        self.quantity.data = item.quantity

    def make_object(self):
        return Item(description=self.description.data, location_id=self.location.data,
                    quantity=self.quantity.data)

    def update_object(self, item):
        item.description = self.description.data
        item.location_id = self.location.data
        item.quantity = self.quantity.data
