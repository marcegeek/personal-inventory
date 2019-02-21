import functools
import locale

from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.usermodel import UserModel


@functools.total_ordering
class User(BusinessEntity):
    """Entidad usuario de la capa de negocio."""

    def __init__(self, id=None, firstname=None, lastname=None,
                 email=None, username=None, password=None,
                 language=None):
        super().__init__(id)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.language = language
        self.locations = None
        self.items = None

    def __eq__(self, other):
        o1 = (self.id, self.firstname, self.lastname, self.email, self.username,
              self.password, self.language, self.locations, self.items)
        o2 = (other.id, other.firstname, other.lastname, other.email, other.username,
              other.password, other.language, other.locations, other.items)
        return o1 == o2

    def __lt__(self, other):
        o1 = (locale.strxfrm(self.lastname), locale.strxfrm(self.firstname))
        o2 = (locale.strxfrm(other.lastname), locale.strxfrm(other.firstname))
        return o1 < o2

    @classmethod
    def make_from_model(cls, usermodel, populate_locations=False, populate_items=False):
        """
        Generar un objeto usuario de negocio a partir del modelo.
        Pudiendo rellenar las relaciones con sus ubicaciones y/o sus
        ítems.

        Las relaciones no se rellenan de manera recursiva.

        :type usermodel: UserModel | list of UserModel
        :type populate_locations: bool
        :type populate_items: bool
        :rtype: User | list of User
        """
        if isinstance(usermodel, list):
            users = [cls.make_from_model(um, populate_locations, populate_items) for um in usermodel]
            users.sort()
            return users
        if usermodel is None:
            return None
        user = cls(usermodel.id, usermodel.firstname, usermodel.lastname,
                   usermodel.email, usermodel.username, usermodel.password,
                   usermodel.language)
        if populate_locations:
            from personal_inventory.business.entities.location import Location
            user.locations = Location.make_from_model(usermodel.locations)
            user.locations.sort()
        if populate_items:
            from personal_inventory.business.entities.item import Item
            user.items = Item.make_from_model(usermodel.items)
            user.items.sort()
        return user

    def to_model(self):
        """
        Generar un objeto usuario del modelo desde el objeto de negocio.

        El objeto generado no incluye las relaciones con otros objetos.

        :rtype: UserModel
        """
        usermodel = UserModel(id=self.id)
        self.update_model(usermodel)
        return usermodel

    def update_model(self, usermodel):
        """
        Modificar un objeto usuario del modelo desde el objeto de negocio.
        El id no se modifica.

        Las relaciones con otros objetos no se modifican.

        :type usermodel: UserModel
        """
        usermodel.firstname = self.firstname
        usermodel.lastname = self.lastname
        usermodel.email = self.email
        usermodel.username = self.username
        usermodel.password = self.password
        usermodel.language = self.language
