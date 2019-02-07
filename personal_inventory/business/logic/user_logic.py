import re

import email_validator

from personal_inventory.business.entities.user import User
from personal_inventory.business.logic import RequiredFieldError, RepeatedUniqueField, \
    DeleteForeingKeyError, InvalidLength, EntityLogic, FieldValidationError
from personal_inventory.business.logic import ValidationError
from personal_inventory.data.data import UserData


class InvalidEmailError(FieldValidationError):

    def __init__(self):
        super().__init__('email')

    def __str__(self):
        return 'Invalid e-mail address'


class RepeatedEmailError(RepeatedUniqueField):

    def __init__(self):
        super().__init__('email')

    def __str__(self):
        return 'E-mail address is repeated'


class RepeatedUsernameError(RepeatedUniqueField):

    def __init__(self):
        super().__init__('username')

    def __str__(self):
        return 'Username is repeated'


class InvalidUsernameError(FieldValidationError):

    def __init__(self):
        super().__init__('username')

    def __str__(self):
        fmt_str = '{0} must be made of lowercase letters, digits and underscores'
        return fmt_str.format(self.field)


class UserLogic(EntityLogic):
    NAME_LEN = (2, 15)
    EMAIL_LEN = (3, 50)
    USERNAME_LEN = (5, 50)
    PASSWORD_LEN = (6, 30)

    def __init__(self):
        super().__init__()
        self.dao = UserData()
        self.plain_object_factory = User

    def get_by_email(self, email):
        """
        Recuperar un usuario dado su email.

        :type email: str
        :rtype: User | None
        """
        return User.make_from_model(self.dao.get_by_email(email))

    def get_by_username(self, username):
        """
        Recuperar un usuario dado su nombre de usuario.

        :type username: str
        :rtype: User | None
        """
        return User.make_from_model(self.dao.get_by_username(username))

    def get_by_username_email(self, username_email):
        """
        Recuperar un usuario dado su nombre de usuario o e-mail.

        :type username_email: str
        :rtype: User | None
        """
        return User.make_from_model(self.dao.get_by_username_email(username_email))

    def validate_login(self, username_email, password):
        """
        Validar login de usuario por nombre de usuario/e-mail y contraseña.

        :type username_email: str
        :type password: str
        :rtype: bool
        """
        user = self.get_by_username_email(username_email)
        if user is not None and user.password == password:
            return True
        # user is None or user.password != password
        return False

    def validate_deletion_fk_rules(self, user_id, errors):
        """
        Validar las reglas de eliminación.

        :type user_id: int
        :type errors: list of ValidationError
        :rtype: bool
        """
        user = self.get_by_id(user_id)
        if user is not None:
            from personal_inventory.business.logic.item_logic import ItemLogic
            from personal_inventory.business.logic.location_logic import LocationLogic

            if len(ItemLogic().get_all_by_user(user)):
                errors.append(DeleteForeingKeyError())
                return False
            if len(LocationLogic().get_all_by_user(user)):
                errors.append(DeleteForeingKeyError())
                return False
        return True  # no importa si el usuario no existe

    def validate_all_rules(self, user, errors):
        """
        Validar todas las reglas de negocio.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        errors.clear()
        present_fields = self.get_present_fields(user)
        self.rule_required_fields(errors, present_fields)
        if 'email' in present_fields and self.rule_email_len(user, errors) and \
                self.rule_valid_email(user, errors):
            self.rule_unique_email(user, errors)
        if 'username' in present_fields and self.rule_username_len(user, errors) and \
                self.rule_valid_username(user, errors):
            self.rule_unique_username(user, errors)
        if 'firstname' in present_fields:
            self.rule_firstname_len(user, errors)
        if 'lastname' in present_fields:
            self.rule_lastname_len(user, errors)
        if 'password' in present_fields:
            self.rule_password_len(user, errors)

        if len(errors) == 0:
            return True
        return False

    @staticmethod
    def get_present_fields(user):
        present_fields = []
        if user.firstname:
            present_fields.append('firstname')
        if user.lastname:
            present_fields.append('lastname')
        if user.email:
            present_fields.append('email')
        if user.username:
            present_fields.append('username')
        if user.password:
            present_fields.append('password')
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
        if 'firstname' not in present_fields:
            field_errors.append(RequiredFieldError('firstname'))
        if 'lastname' not in present_fields:
            field_errors.append(RequiredFieldError('lastname'))
        if 'email' not in present_fields:
            field_errors.append(RequiredFieldError('email'))
        if 'username' not in present_fields:
            field_errors.append(RequiredFieldError('username'))
        if 'password' not in present_fields:
            field_errors.append(RequiredFieldError('password'))
        if len(field_errors) == 0:
            return True
        for f in field_errors:
            errors.append(f)
        return False

    def rule_unique_email(self, user, errors):
        """
        Validar que el e-mail del usuario es único.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        enc = self.dao.get_by_email(user.email)
        if enc is None or enc.id == user.id:
            return True
        errors.append(RepeatedEmailError())
        return False

    def rule_unique_username(self, user, errors):
        """
        Validar que el nombre de usuario del usuario es único.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        enc = self.dao.get_by_username(user.username)
        if enc is None or enc.id == user.id:
            return True
        errors.append(RepeatedUsernameError())
        return False

    @classmethod
    def rule_firstname_len(cls, user, errors):
        """
        Validar que el nombre del usuario cuente con al menos 2 caracteres
        y no más de 15.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not cls.NAME_LEN[0] <= len(user.firstname) <= cls.NAME_LEN[1]:
            errors.append(InvalidLength('firstname', cls.NAME_LEN))
            return False
        return True

    @classmethod
    def rule_lastname_len(cls, user, errors):
        """
        Validar que el apellido del usuario cuente con al menos 2 caracteres
        y no más de 15.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not cls.NAME_LEN[0] <= len(user.lastname) <= cls.NAME_LEN[1]:
            errors.append(InvalidLength('lastname', cls.NAME_LEN))
            return False
        return True

    @classmethod
    def rule_email_len(cls, user, errors):
        """
        Validar que el e-mail del usuario cuente con al menos 3 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if cls.EMAIL_LEN[0] <= len(user.email) <= cls.EMAIL_LEN[1]:
            return True
        errors.append(InvalidLength('email', cls.EMAIL_LEN))
        return False

    @staticmethod
    def rule_valid_email(user, errors):
        """
        Validar que el e-mail del usuario sea una dirección válida.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        try:
            # validar e-mail (sólo el formato de la dirección)
            email_validator.validate_email(user.email, check_deliverability=False)
            return True
        except email_validator.EmailNotValidError:
            errors.append(InvalidEmailError())
            return False

    @classmethod
    def rule_username_len(cls, user, errors):
        """
        Validar que el nombre de usuario cuente con al menos 5 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if cls.USERNAME_LEN[0] <= len(user.username) <= cls.USERNAME_LEN[1]:
            return True
        errors.append(InvalidLength('username', cls.USERNAME_LEN))
        return False

    @staticmethod
    def rule_valid_username(user, errors):
        """
        Validar que el nombre de usuario sea válido:
        minúsculas, números y guiones bajos

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if re.fullmatch('[a-z0-9_]+', user.username):
            return True
        errors.append(InvalidUsernameError())
        return False

    @classmethod
    def rule_password_len(cls, user, errors):
        """
        Validar que la contraseña cuente con al menos 6 caracteres
        y no más de 30.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if cls.PASSWORD_LEN[0] <= len(user.password) <= cls.PASSWORD_LEN[1]:
            return True
        errors.append(InvalidLength('password', cls.PASSWORD_LEN))
        return False
