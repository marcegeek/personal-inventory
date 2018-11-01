from personal_inventory.logic.user_logic import UserLogic

from personal_inventory.logic import ObjectLogic, RequiredFieldError, ValidationError, ForeignKeyError, \
    InvalidLengthError

from personal_inventory.data.data import LocationData


class LocationLogic(ObjectLogic):
    DESCRIPTION_LEN = (3, 50)

    def __init__(self):
        super().__init__()
        self.dao = LocationData()

    def get_all_by_user(self, user):
        """
        Recuperar todas las ubicaciones pertenecientes a un usuario.

        :type user: User
        :rtype: list of Location
        """
        return self.dao.get_all_by_user(user)

    def validate_all_rules(self, location, errors):
        """
        Validar todas las reglas de negocio.

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

        if len(errors) == 0:
            return True
        return False

    def get_present_fields(self, location):
        present_fields = []
        if location.owner_id:
            present_fields.append('owner_id')
        if location.description:
            present_fields.append('description')
        return present_fields

    def rule_required_fields(self, errors, present_fields):
        """
        Validar la presencia de los campos requeridos, dada la lista de los presentes.

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

    def rule_owner_user_exists(self, location, errors):
        """
        Validar que existe el usuario que administra la ubicación.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        ul = UserLogic()
        if ul.get_by_id(location.owner_id) is None:
            errors.append(ForeignKeyError('owner_id'))
        return True

    def rule_description_len(self, location, errors):
        """
        Validar que la descripción de la ubicación cuente con al menos 3 caracteres
        y no más de 50.

        :type location: Location
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not self.DESCRIPTION_LEN[0] <= len(location.description) <= self.DESCRIPTION_LEN[1]:
            errors.append(InvalidLengthError('description', self.DESCRIPTION_LEN))
            return False
        return True
