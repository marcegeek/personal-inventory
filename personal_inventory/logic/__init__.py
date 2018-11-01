class ValidationError:

    def __init__(self, field):
        self.field = field


class RequiredFieldError(ValidationError):

    def __init__(self, field):
        super().__init__(field)

    def __str__(self):
        return '{0} is required'.format(self.field)


class RepeatedUniqueField(ValidationError):

    def __init__(self, field):
        super().__init__(field)

    def __str__(self):
        return '{0} is repeated'.format(self.field)


class ValidationException(Exception):
    pass


class ObjectLogic:

    def __init__(self):
        self.dao = None  # reemplazar en las subclases

    def get_by_id(self, object_id):
        """
        Recuperar un objeto del modelo dado su id.

        :type object_id: int
        :rtype: Model | None
        """
        return self.dao.get_by_id(object_id)

    def get_all(self):
        """
        Recuperar todos los objetos del modelo.

        :rtype: list of Model
        """
        return self.dao.get_all()

    def insert(self, obj):
        """
        Dar de alta un objeto del modelo.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type obj: Model
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        if self.validate_all_rules(obj, errors):
            self.dao.insert(obj)
            return True
        raise ValidationException(*errors)

    def update(self, obj):
        """
        Modfificar un objeto del modelo.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type obj: Model
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        if self.validate_all_rules(obj, errors):
            self.dao.update(obj)
            return True
        raise ValidationException(errors)

    def delete(self, object_id):
        """
        Dar de baja un objeto del modelo según su id.

        :type object_id: int
        :rtype: bool
        """
        return self.dao.delete(object_id)

    def validate_all_rules(self, obj, errors):
        return False  # reemplazar en las subclases
