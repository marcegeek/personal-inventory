from personal_inventory.business.entities import BusinessEntity
from personal_inventory.data.models.usermodel import UserModel


class User(BusinessEntity):

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

    @classmethod
    def make_from_model(cls, usermodel, **fill_relations):
        """
        Generar un objeto usuario de negocio a partir del modelo.

        :type usermodel: UserModel | list of UserModel
        :rtype: User | list of User
        """
        if isinstance(usermodel, list):
            return [cls.make_from_model(um, **fill_relations) for um in usermodel]
        if usermodel is None:
            return None
        user = cls(usermodel.id, usermodel.firstname, usermodel.lastname,
                   usermodel.email, usermodel.username, usermodel.password,
                   usermodel.language)
        if 'fill_locations' in fill_relations:
            from personal_inventory.business.entities.location import Location
            user.locations = Location.make_from_model(usermodel.locations)
        if 'fill_items' in fill_relations:
            from personal_inventory.business.entities.item import Item
            user.items = Item.make_from_model(usermodel.items)
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

        :type usermodel: UserModel
        """
        usermodel.firstname = self.firstname
        usermodel.lastname = self.lastname
        usermodel.email = self.email
        usermodel.username = self.username
        usermodel.password = self.password
        usermodel.language = self.language
