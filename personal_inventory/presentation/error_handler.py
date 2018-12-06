import flask_babel

from personal_inventory.business.logic import RequiredFieldError, ForeignKeyError, DeleteForeingKeyError, InvalidLength
from personal_inventory.business.logic.item_logic import InvalidValue
from personal_inventory.business.logic.location_logic import RepeatedLocationNameError
from personal_inventory.business.logic.user_logic import InvalidEmailError, RepeatedUsernameError, InvalidUsernameError


def error_str(error):
    if isinstance(error, RequiredFieldError):
        return flask_babel.gettext('%(field)s is required', field=error.field)  # FIXME too generic
    elif isinstance(error, ForeignKeyError):
        return flask_babel.gettext("%(field)s foreign key doesn't exist", field=error.field)  # FIXME too generic
    elif isinstance(error, DeleteForeingKeyError):
        return flask_babel.gettext('Still some %(field)s referencing object', field=error.field)  # FIXME too generic
    elif isinstance(error, InvalidLength):
        return flask_babel.gettext('%{field}s length must be between %(min)d and %(max)d',
                                   field=error.field, min=error.range[0], max=error.range[1])
    elif isinstance(error, InvalidEmailError):
        return flask_babel.gettext('Invalid e-mail address')
    elif isinstance(error, RepeatedUsernameError):
        return flask_babel.gettext('Username is repeated')
    elif isinstance(error, InvalidUsernameError):
        return flask_babel.gettext('Username must be made of lowercase letters, digits and underscores')
    elif isinstance(error, RepeatedLocationNameError):
        return flask_babel.gettext('Location name repeated')
    elif isinstance(error, InvalidValue):
        return flask_babel.gettext('%(field)s value is invalid', field=error.field)  # FIXME too generic
    else:
        return str(error)  # fallback
