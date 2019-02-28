from flask_babel import gettext as _

from personal_inventory.business.logic import RequiredFieldError, DeleteForeingKeyError, InvalidLength
from personal_inventory.business.logic.item_logic import InvalidValue, RepeatedItemNameError
from personal_inventory.business.logic.location_logic import RepeatedLocationNameError
from personal_inventory.business.logic.user_logic import InvalidEmailError, RepeatedUsernameError, InvalidUsernameError


def error_str(error):
    """Generar mensaje a partir de un error de la capa de negocio"""

    if isinstance(error, RequiredFieldError):
        return _('Required field')
    elif isinstance(error, DeleteForeingKeyError):
        return _("There's still some object referencing this")
    elif isinstance(error, InvalidLength):
        return _('Invalid field length')
    elif isinstance(error, InvalidEmailError):
        return _('Invalid e-mail address')
    elif isinstance(error, RepeatedUsernameError):
        return _('Username is repeated')
    elif isinstance(error, InvalidUsernameError):
        return _('Username must be made of lowercase letters, digits and underscores')
    elif isinstance(error, RepeatedLocationNameError):
        return _('Location name repeated')
    elif isinstance(error, RepeatedItemNameError):
        return _('Item name repeated')
    elif isinstance(error, InvalidValue):
        return _('Invalid value')
    else:
        return str(error)  # fallback, sin localización
