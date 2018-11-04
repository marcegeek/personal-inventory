"""
Mapeo de objetos del modelo a objetos planos.

Esto es para evitar inconvenientes al utilizar directamente los modelos
de SQLAlchemy.
"""

import abc

from personal_inventory.data.models import UserModel, LocationModel, ItemModel


class PlainObject(abc.ABC):
    """Objeto plano de la capa lógica."""

    def __init__(self, id=None):
        self.id = id

    @classmethod
    @abc.abstractmethod
    def make_from_model(cls, modelobject):
        pass

    @abc.abstractmethod
    def to_model(self):
        pass

    @abc.abstractmethod
    def update_model(self, modelobject):
        pass


class User(PlainObject):

    def __init__(self, id=None, firstname=None, lastname=None,
                 email=None, username=None, password=None):
        super().__init__(id)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password

    @classmethod
    def make_from_model(cls, usermodel):
        """
        Generar un objeto usuario plano a partir del modelo.

        :type usermodel: UserModel
        :rtype: User
        """
        if usermodel is None:
            return None
        user = cls(usermodel.id, usermodel.firstname, usermodel.lastname,
                   usermodel.email, usermodel.username, usermodel.password)
        return user

    def to_model(self):
        """
        Generar un objeto usuario del modelo desde el objeto plano.

        :rtype: UserModel
        """
        return UserModel(id=self.id, firstname=self.firstname, lastname=self.lastname,
                         email=self.email, username=self.username, password=self.password)

    def update_model(self, usermodel):
        """
        Modificar un objeto usuario del modelo desde el objeto plano.
        El id no se modifica.

        :type usermodel: UserModel
        """
        usermodel.firstname = self.firstname
        usermodel.lastname = self.lastname
        usermodel.email = self.email
        usermodel.username = self.username
        usermodel.password = self.password


class Location(PlainObject):

    def __init__(self, id=None, owner_id=None, description=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description

    @classmethod
    def make_from_model(cls, locationmodel):
        """
        Generar un objeto ubicación plano a partir del modelo.

        :type locationmodel: LocationModel
        :rtype: Location
        """
        if locationmodel is None:
            return None
        location = cls(locationmodel.id, locationmodel.owner_id, locationmodel.description)
        return location

    def to_model(self):
        """
        Generar un objeto ubicación del modelo desde el objeto plano.

        :rtype: LocationModel
        """
        return LocationModel(id=self.id, owner_id=self.owner_id,
                             description=self.description)

    def update_model(self, locationmodel):
        """
        Modificar un objeto ubicación del modelo desde el objeto plano.
        El id no se modifica.

        :type locationmodel: LocationModel
        """
        locationmodel.owner_id = self.owner_id
        locationmodel.description = self.description


class Item(PlainObject):

    def __init__(self, id=None, owner_id=None, description=None, location_id=None, quantity=None):
        super().__init__(id)
        self.owner_id = owner_id
        self.description = description
        self.location_id = location_id
        self.quantity = quantity

    @classmethod
    def make_from_model(cls, itemmodel):
        """
        Generar un objeto ítem plano a partir del modelo.

        :type itemmodel: ItemModel
        :return: Item
        """
        if itemmodel is None:
            return None
        item = cls(itemmodel.id, itemmodel.owner_id, itemmodel.description,
                   itemmodel.location_id, itemmodel.quantity)
        return item

    def to_model(self):
        """
        Generar un objeto ítem del modelo desde el objeto plano.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: ItemModel
        """
        return ItemModel(id=self.id, owner_id=self.owner_id, location_id=self.location_id,
                         description=self.description, quantity=self.quantity)

    def update_model(self, itemmodel):
        """
        Modificar un objeto ítem del modelo desde el objeto plano.
        El id no se modifica.

        :type itemmodel: ItemModel
        """
        itemmodel.owner_id = self.owner_id
        itemmodel.description = self.description
        itemmodel.location_id = self.location_id
        itemmodel.quantity = self.quantity
