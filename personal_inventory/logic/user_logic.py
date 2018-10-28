import email_validator
import re

from personal_inventory.data.data import UserData
from personal_inventory.logic import ValidationError, RepeatedUniqueField, RequiredFieldError


class InvalidEmailError(ValidationError):

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


class InvalidLengthError(ValidationError):

    def __init__(self, field, len_range):
        super().__init__(field)
        self.range = len_range

    def __str__(self):
        fmt_str = '{0} length must be between {1} and {2}'
        return fmt_str.format(self.field, self.range[0], self.range[1])


class InvalidUsernameError(ValidationError):

    def __init__(self):
        super().__init__('username')

    def __str__(self):
        fmt_str = '{0} must be made of lowercase letters, digits and underscores'
        return fmt_str.format(self.field)


class ValidationException(Exception):
    pass


class UserLogic:
    NAME_LEN = (2, 50)
    EMAIL_LEN = (3, 50)
    USERNAME_LEN = (5, 50)
    PASSWORD_LEN = (6, 30)

    def __init__(self):
        self.dao = UserData()

    def get_by_id(self, user_id):
        """
        Recuperar un usuario dado su id.

        :type user_id: int
        :param user_id: id del usuario a recuperar
        :return: usuario con ese id o None si no existe
        :rtype: User | None
        """
        return self.dao.get_by_id(user_id)

    def get_by_email(self, email):
        """
        Recuperar un usuario dado su email.

        :type email: str
        :param email: email del usuario a recuperar
        :return: usuario con ese email o None si no existe
        :rtype: User | None
        """
        return self.dao.get_by_email(email)

    def get_by_username(self, username):
        """
        Recuperar un usuario dado su nombre de usuario.

        :type username: str
        :param username: nombre de usuario del usuario a recuperar
        :return: usuario con ese email o None si no existe
        :rtype: User | None
        """
        return self.dao.get_by_username(username)

    def get_by_username_email(self, username_email):
        """
        Recuperar un usuario dado su nombre de usuario o e-mail.

        :type username_email: str
        :rtype: User | None
        """
        return self.dao.get_by_username_email(username_email)

    def get_all(self):
        """
        Recuperar todos los usuarios.

        :return: listado de todos los usuarios.
        :rtype: list of User
        """
        return self.dao.get_all()

    def insert(self, user):
        """
        Dar de alta un usuario.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type user: User
        :return: True si el alta fue exitoso
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        present_fields = []

        self.rule_required_fields(user, errors, present_fields)
        if 'email' in present_fields and self.rule_email_len(user, errors) and \
                self.rule_valid_email(user, errors):
            self.rule_unique_email(user, errors)
        if 'username' in present_fields and self.rule_username_len(user, errors):
            self.rule_unique_username(user, errors)
        if 'firstname' in present_fields:
            self.rule_firstname_len(user, errors)
            self.rule_valid_username(user, errors)
        if 'lastname' in present_fields:
            self.rule_lastname_len(user, errors)

        if len(errors) == 0:
            self.dao.insert(user)
            return True
        raise ValidationException(*errors)

    def update(self, user):
        """
        Modfificar un usuario.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type user: User
        :return: True si la modificación fue exitosa
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        present_fields = []

        self.rule_required_fields(user, errors, present_fields)
        if 'email' in present_fields and self.rule_email_len(user, errors) and \
                self.rule_valid_email(user, errors):
            self.rule_unique_email(user, errors)
        if 'username' in present_fields and self.rule_username_len(user, errors):
            self.rule_unique_username(user, errors)
        if 'firstname' in present_fields:
            self.rule_firstname_len(user, errors)
        if 'lastname' in present_fields:
            self.rule_lastname_len(user, errors)

        if len(errors) == 0:
            self.dao.update(user)
            return True
        raise ValidationException(errors)

    def delete(self, user_id):
        pass

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

    def rule_required_fields(self, user, errors, present_fields):
        """
        Validar la presencia de los campos requeridos.

        :type user: User
        :type errors: list of ValidationError
        :type present_fields: list of str
        :rtype: bool
        """
        field_errors = []
        if user.firstname:
            present_fields.append('firstname')
        else:
            field_errors.append(RequiredFieldError('firstname'))
        if user.lastname:
            present_fields.append('lastname')
        else:
            field_errors.append(RequiredFieldError('lastname'))
        if user.email:
            present_fields.append('email')
        else:
            field_errors.append(RequiredFieldError('email'))
        if user.username:
            present_fields.append('username')
        else:
            field_errors.append(RequiredFieldError('username'))
        if user.password:
            present_fields.append('password')
        else:
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

    def rule_firstname_len(self, user, errors):
        """
        Validar que el nombre del usuario cuente con al menos 2 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not self.NAME_LEN[0] <= len(user.firstname) <= self.NAME_LEN[1]:
            errors.append(InvalidLengthError('firstname', self.NAME_LEN))
            return False
        return True

    def rule_lastname_len(self, user, errors):
        """
        Validar que el apellido del usuario cuente con al menos 2 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if not self.NAME_LEN[0] <= len(user.lastname) <= self.NAME_LEN[1]:
            errors.append(InvalidLengthError('lastname', self.NAME_LEN))
            return False
        return True

    def rule_email_len(self, user, errors):
        """
        Validar que el e-mail del usuario cuente con al menos 3 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if self.EMAIL_LEN[0] <= len(user.email) <= self.EMAIL_LEN[1]:
            return True
        errors.append(InvalidLengthError('email', self.EMAIL_LEN))
        return False

    def rule_valid_email(self, user, errors):
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

    def rule_username_len(self, user, errors):
        """
        Validar que el nombre de usuario cuente con al menos 5 caracteres
        y no más de 50.

        :type user: User
        :type errors: list of ValidationError
        :rtype: bool
        """
        if self.USERNAME_LEN[0] <= len(user.username) <= self.USERNAME_LEN[1]:
            return True
        errors.append(InvalidLengthError('username', self.USERNAME_LEN))
        return False

    def rule_valid_username(self, user, errors):
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
