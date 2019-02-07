from flask_babel import lazy_gettext as _
from wtforms import StringField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms import validators

from personal_inventory.business.logic.item_logic import ItemLogic
from personal_inventory.presentation.views.forms import BaseForm


class ItemForm(BaseForm):
    description = StringField(_('Description'), description=_('Field length must be between %(min)d and %(max)d', min=ItemLogic.DESCRIPTION_LEN[0], max=ItemLogic.DESCRIPTION_LEN[1]),
                              render_kw={'aria-describedby': 'description-description'})
    location = SelectField(_('Location'))
    quantity = IntegerField(_('Quantity'), description=_('Optional field, must be a non-negative integer number'),
                            render_kw={'aria-describedby': 'quantity-description'},
                            validators=[validators.Optional()])
