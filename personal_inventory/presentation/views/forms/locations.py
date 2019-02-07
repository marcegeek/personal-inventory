from flask_babel import lazy_gettext as _
from wtforms import StringField

from personal_inventory.business.logic.location_logic import LocationLogic
from personal_inventory.presentation.views.forms import BaseForm


class LocationForm(BaseForm):
    description = StringField(_('Description'), description=_('Field length must be between %(min)d and %(max)d', min=LocationLogic.DESCRIPTION_LEN[0], max=LocationLogic.DESCRIPTION_LEN[1]),
                              render_kw={'aria-describedby': 'description-description'})
