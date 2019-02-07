from wtforms import StringField

from personal_inventory.presentation.views.forms import BaseForm


class LocationForm(BaseForm):
    description = StringField('Description')
