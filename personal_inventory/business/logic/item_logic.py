import datetime

from personal_inventory.business.entities.item import Item
from personal_inventory.business.logic import RequiredFieldError, ForeignKeyError, InvalidLength, EntityLogic, \
    ValidationException, DeleteForeingKeyError, RepeatedUniqueField
from personal_inventory.business.logic import ValidationError
from personal_inventory.data.data import ItemData


class InvalidValue(ValidationError):

    def __str__(self):
        return '{0} value is invalid'.format(self.field)


class ItemLogic(EntityLogic):
    DESCRIPTION_LEN = (3, 50)

    def __init__(self):
        super().__init__()
        self.dao = ItemData()
        self.plain_object_factory = Item

    def get_all_by_user(self, user, fill_location=False):
        """
        Recuperar todos los ítems pertenecientes a un usuario.

        :type user: User
        :type fill_location: bool
        :rtype: list of Item
        """
        item_list = [Item.make_from_model(im) for im in self.dao.get_all_by_user(user)]
        if fill_location:
            from personal_inventory.business.logic.location_logic import LocationLogic
            for item in item_list:
                item.location = LocationLogic().get_by_id(item.id)
        return item_list

    def get_all_by_location(self, location, fill_location=False):
        """
        Recuperar todos los ítems que están en una ubicación.

        :type location: Location
        :type fill_location: bool
        :rtype: list of Item
        """
        item_list = [Item.make_from_model(im) for im in self.dao.get_all_by_location(location)]
        if fill_location:
            for item in item_list:
                item.location = location
        return item_list

    def validate_deletion_fk_rules(self, item_id, errors):
        """
        Validar las reglas de eliminación.

        :type item_id: int
        :type errors: list of ValidationError
        :rtype: bool
        """
        return True  # nada depende del ítem

    def validate_all_rules(self, item, errors):
        """
        Validar todas las reglas de negocio.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        errors.clear()
        present_fields = self.get_present_fields(item)
        self.rule_required_fields(errors, present_fields)
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

    @staticmethod
    def get_present_fields(item):
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

    @staticmethod
    def rule_required_fields(errors, present_fields):
        """
        Validar la presencia de los campos requeridos, dada la lista de los presentes.

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

    @staticmethod
    def rule_owner_user_exists(item, errors):
        """
        Validar que existe el usuario propietario del item.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        from personal_inventory.business.logic.user_logic import UserLogic
        ul = UserLogic()
        if ul.get_by_id(item.owner_id) is None:
            errors.append(ForeignKeyError('owner_id'))
        return True

    @staticmethod
    def rule_location_exists(item, errors):
        """
        Validar que existe la ubicación del ítem.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        from personal_inventory.business.logic.location_logic import LocationLogic
        ll = LocationLogic()
        if ll.get_by_id(item.location_id) is None:
            errors.append(ForeignKeyError('location_id'))
        return True

    @classmethod
    def rule_description_len(cls, item, errors):
        """
        Validar que la descripción del ítem cuente con al menos 3 caracteres
        y no más de 50.

        :type item: Item
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not cls.DESCRIPTION_LEN[0] <= len(item.description) <= cls.DESCRIPTION_LEN[1]:
            errors.append(InvalidLength('description', cls.DESCRIPTION_LEN))
            return False
        return True

    @staticmethod
    def rule_valid_quantity(item, errors):
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
        except ValueError:
            pass  # ignorar
        except TypeError:
            pass
        # si validó ya salió retornando True
        errors.append(InvalidValue('quantity'))
        return False
