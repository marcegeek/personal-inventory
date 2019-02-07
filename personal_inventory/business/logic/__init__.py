import abc

from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.data import ObjectData


class ValidationError:
    pass


class FieldValidationError(ValidationError):

    def __init__(self, field):
        self.field = field


class RequiredFieldError(FieldValidationError):

    def __init__(self, field):
        super().__init__(field)

    def __str__(self):
        return '{0} is required'.format(self.field)


class RepeatedUniqueField(FieldValidationError):

    def __str__(self):
        return '{0} is repeated'.format(self.field)


class ForeignKeyError(ValidationError):

    def __init__(self, foreign_entity):
        self.foreign_entity = foreign_entity

    def __str__(self):
        return "{0} foreign key doesn't exist".format(self.foreign_entity)


class DeleteForeingKeyError(ValidationError):

    def __str__(self):
        return "There's still some object referencing this"


class InvalidLength(FieldValidationError):

    def __init__(self, field, len_range):
        super().__init__(field)
        self.range = len_range

    def __str__(self):
        fmt_str = '{0} length must be between {1} and {2}'
        return fmt_str.format(self.field, self.range[0], self.range[1])


class ValidationException(Exception):
    pass


class EntityLogic(abc.ABC):

    def __init__(self):
        self.dao = ObjectData()  # reemplazar en las subclases
        self.plain_object_factory = BusinessEntity  # reemplazar en las subclases

    def get_by_id(self, object_id, **fill_relations):
        """
        Recuperar un objeto del modelo dado su id.

        :type object_id: int
        :type fill_relations: dict of bool
        :rtype: BusinessEntity | None
        """
        return self.plain_object_factory.make_from_model(self.dao.get_by_id(object_id), **fill_relations)

    def get_all(self, **fill_relations):
        """
        Recuperar todos los objetos del modelo.

        :rtype: list of BusinessEntity
        :type fill_relations: dict of bool
        """
        return self.plain_object_factory.make_from_model(self.dao.get_all(), **fill_relations)

    def insert(self, obj):
        """
        Dar de alta un objeto de negocio en el modelo.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type obj: BusinessEntity
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        if self.validate_all_rules(obj, errors):
            om = self.dao.insert(obj.to_model())
            obj.id = om.id
            return True
        raise ValidationException(*errors)

    def update(self, obj):
        """
        Modfificar un objeto de negocio en el modelo.

        Primero se deben validar las reglas de negocio.
        Si no validan, levantar una excepción con los
        errores de validación correspondientes.

        :type obj: BusinessEntity
        :rtype: bool
        :raise: ValidationException
        """
        errors = []
        if self.validate_all_rules(obj, errors):
            model_object = self.dao.get_by_id(obj.id)
            if model_object is None:
                return False
            obj.update_model(model_object)
            self.dao.update(model_object)
            return True
        raise ValidationException(*errors)

    def delete(self, object_id):
        """
        Dar de baja un objeto del modelo según su id.

        Primero se deben validar las reglas de eliminación
        (no romper claves foráneas obligatorias de otros objetos).

        :type object_id: int
        :rtype: bool
        """
        errors = []
        if self.validate_deletion_fk_rules(object_id, errors):
            return self.dao.delete(object_id)
        raise ValidationException(*errors)

    @abc.abstractmethod
    def validate_all_rules(self, obj, errors):
        pass

    @abc.abstractmethod
    def validate_deletion_fk_rules(self, object_id, errors):
        pass
