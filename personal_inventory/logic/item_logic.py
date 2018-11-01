from personal_inventory.logic.location_logic import LocationLogic
from personal_inventory.logic.user_logic import UserLogic

from personal_inventory.data.data import ItemData
from personal_inventory.logic import ObjectLogic, RequiredFieldError, ForeignKeyError, InvalidLengthError, \
    ValidationError


class InvalidValueError(ValidationError):

    def __str__(self):
        return '{0} value is invalid'.format(self.field)


class ItemLogic(ObjectLogic):
    DESCRIPTION_LEN = (3, 50)

    def __init__(self):
        super().__init__()
        self.dao = ItemData()

    def get_all_by_user(self, user):
        """
        Recuperar todos los ítems pertenecientes a un usuario.

        :type user: User
        :rtype: list of Item
        """
        return self.dao.get_all_by_user(user)

    def get_all_by_location(self, location):
        """
        Recuperar todos los ítems que están en una ubicación.

        :type location: Location
        :rtype: list of Item
        """
        return self.dao.get_all_by_location()

    def validate_all_rules(self, item, errors):
        """
        Validar todas las reglas de negocio.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        errors.clear()
        present_fields = self.get_present_fields(item)
        self.rule_required_fields(item, errors, present_fields)
        if 'owner_id' in present_fields:
            self.rule_owner_user_exists(item, errors)
        if 'location_id' in present_fields:
            self.rule_location_exists(item, errors)
        if 'description' in present_fields:
            self.rule_description_len(item, errors)
        if 'quantity' in present_fields:
            self.rule_valid_quantity(item, errors)

        if len(errors) == 0:
            return True
        return False

    def get_present_fields(self, item):
        present_fields = []
        if item.owner_id:
            present_fields.append('owner_id')
        if item.location_id:
            present_fields.append('location_id')
        if item.description:
            present_fields.append('description')
        if item.quantity is not None:  # puede ser 0
            present_fields.append('quantity')
        return present_fields

    def rule_required_fields(self, item, errors, present_fields):
        """
        Validar la presencia de los campos requeridos, dada la lista de los presentes.

        :type item: Item
        :type errors: list of ValidationError
        :type present_fields: list of str
        :rtype: bool
        """
        field_errors = []
        if 'owner_id' not in present_fields:
            field_errors.append(RequiredFieldError('owner_id'))
        if 'location_id' not in present_fields:
            field_errors.append(RequiredFieldError('location_id'))
        if 'description' not in present_fields:
            field_errors.append(RequiredFieldError('description'))
        if len(field_errors) == 0:
            return True
        for f in field_errors:
            errors.append(f)
        return False

    def rule_owner_user_exists(self, item, errors):
        """
        Validar que existe el usuario propietario del item.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        ul = UserLogic()
        if ul.get_by_id(item.owner_id) is None:
            errors.append(ForeignKeyError('owner_id'))
        return True

    def rule_location_exists(self, item, errors):
        """
        Validar que existe la ubicación del ítem.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        ll = LocationLogic()
        if ll.get_by_id(item.location_id) is None:
            errors.append(ForeignKeyError('location_id'))
        return True

    def rule_description_len(self, item, errors):
        """
        Validar que la descripción del ítem cuente con al menos 3 caracteres
        y no más de 50.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not self.DESCRIPTION_LEN[0] <= len(item.description) <= self.DESCRIPTION_LEN[1]:
            errors.append(InvalidLengthError('description', self.DESCRIPTION_LEN))
            return False
        return True

    def rule_valid_quantity(self, item, errors):
        """
        Validar que la cantidad es un número entero no negativo.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        try:
            q = int(item.quantity)
            if q >= 0:
                return True
        except Exception:
            pass  # ignorar
        # si validó ya salió retornando True
        errors.append(InvalidValueError('quantity'))
        return False
