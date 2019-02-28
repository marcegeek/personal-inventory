from personal_inventory.business.entities.location import Location
from personal_inventory.business.logic import RequiredFieldError, ForeignKeyError, \
    DeleteForeignKeyError, InvalidLength, EntityLogic, RepeatedUniqueField
from personal_inventory.data import LocationData


class RepeatedLocationNameError(RepeatedUniqueField):

    def __init__(self):
        super().__init__('description')

    def __str__(self):
        return 'Location name repeated'


class LocationLogic(EntityLogic):
    """Objeto de la lógica de ubicaciones"""

    DESCRIPTION_LEN = (3, 50)

    def __init__(self):
        super().__init__()
        self.dao = LocationData()
        self.plain_object_factory = Location

    def get_all_by_user(self, user, populate_owner=False, populate_items=False):
        """
        Recuperar todas las ubicaciones pertenecientes a un usuario.

        :type user: User
        :type populate_owner: bool
        :type populate_items: bool
        :rtype: list of Location
        """
        return Location.make_from_model(self.dao.get_all_by_user(user), populate_owner=populate_owner, populate_items=populate_items)

    def validate_deletion_fk_rules(self, location_id, errors):
        """
        Validar las reglas de eliminación.

        En caso de que hubieran ítems referenciando a la ubicación insertar un error de tipo
        DeleteForeignKeyError con la relación 'items'.

        :type location_id: int
        :type errors: list of ValidationError
        :rtype: bool
        """
        location = self.get_by_id(location_id, populate_items=True)
        if location is not None:
            if location.items:
                errors.append(DeleteForeignKeyError('items'))
                return False
        return True  # no importa si la ubicación no existe

    def validate_all_rules(self, location, errors):
        """
        Validar todas las reglas de negocio.

        Reiniciar el listado de errores. En caso de que hubiera errores,
        insertar los errores correspondientes.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        errors.clear()
        present_fields = self.get_present_fields(location)
        self.rule_required_fields(errors, present_fields)
        if 'owner_id' in present_fields:
            self.rule_owner_user_exists(location, errors)
        if 'description' in present_fields:
            self.rule_description_len(location, errors)
            self.rule_unique_description_per_user(location, errors)

        if len(errors) == 0:
            return True
        return False

    @staticmethod
    def get_present_fields(location):
        present_fields = []
        if location.owner_id:
            present_fields.append('owner_id')
        if location.description:
            present_fields.append('description')
        return present_fields

    @staticmethod
    def rule_required_fields(errors, present_fields):
        """
        Validar la presencia de los campos requeridos, dada la lista de los presentes.

        En caso de que falten campos, insertar errores de tipo
        RequiredFieldError con los campos respectivos.

        :type errors: list of ValidationError
        :type present_fields: list of str
        :rtype: bool
        """
        field_errors = []
        if 'owner_id' not in present_fields:
            field_errors.append(RequiredFieldError('owner_id'))
        if 'description' not in present_fields:
            field_errors.append(RequiredFieldError('description'))
        if len(field_errors) == 0:
            return True
        for f in field_errors:
            errors.append(f)
        return False

    @staticmethod
    def rule_owner_user_exists(location, errors):
        """
        Validar que existe el usuario que administra la ubicación.

        En caso de que el usuario no exista insertar un error de tipo
        ForeignKeyError con el campo 'owner_id'.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        from personal_inventory.business.logic.user_logic import UserLogic
        ul = UserLogic()
        if ul.get_by_id(location.owner_id) is None:
            errors.append(ForeignKeyError('owner_id'))
            return False
        return True

    @classmethod
    def rule_description_len(cls, location, errors):
        """
        Validar que la descripción de la ubicación cuente con al menos 3 caracteres
        y no más de 50.

        En caso de que la longitud sea inválida insertar un error de tipo
        InvalidLength con el campo 'description' y el rango válido de la misma.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not cls.DESCRIPTION_LEN[0] <= len(location.description) <= cls.DESCRIPTION_LEN[1]:
            errors.append(InvalidLength('description', cls.DESCRIPTION_LEN))
            return False
        return True

    def rule_unique_description_per_user(self, location, errors):
        """
        Validar que el nombre de la ubicación es única para el usuario correspondiente.

        En caso de que el nombre de la ubicación esté repetido insertar un error de tipo
        RepeatedLocationNameError.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        from personal_inventory.business.entities.user import UserModel
        user_locs = self.dao.get_all_by_user(UserModel(id=location.owner_id))
        for found in user_locs:
            if location.id != found.id and location.description == found.description:
                errors.append(RepeatedLocationNameError())
                return False
        return True
