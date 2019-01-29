from wtforms import StringField

from personal_inventory.presentation.forms import BaseForm


class LocationForm(BaseForm):
    description = StringField('Description')
