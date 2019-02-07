import flask_babel as fl_babel
from wtforms import StringField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms import validators

from personal_inventory.presentation.views.forms import BaseForm


class ItemForm(BaseForm):
    description = StringField(fl_babel.gettext('Description'))
    location = SelectField(fl_babel.gettext('Location'))
    quantity = IntegerField(fl_babel.gettext('Quantity'), validators=[validators.Optional()])
