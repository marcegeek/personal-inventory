from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.orm import sessionmaker

from personal_inventory.data.models import Base, User, Location, Category, Item, Usage

import config

engine = None
db_session = None
configured = False


def configure():
    """
    Configurar la capa de datos.

    Toma la información del módulo config. A la primera instanciación de
    un objeto de acceso a datos esta función es llamada automáticamente.
    """
    global engine
    engine = engine_from_config(config.getdbconf(), prefix='db.')
    Base.metadata.bind = engine
    global db_session
    db_session = sessionmaker()
    db_session.bind = engine
    Base.metadata.create_all(engine)
    global configured
    configured = True


class ObjectData:

    def __init__(self):
        if not configured:
            configure()
        self.session = db_session(autoflush=False)
        self.model = None  # reemplazar en las subclases

    def get_by_id(self, object_id):
        """
        Recuperar un objeto de un modelo dado su id.

        :type object_id: int
        :rtype: Model
        """
        return self.session.query(self.model).filter(self.model.id == object_id).first()

    def get_all(self):
        """
        Recuperar todos los objetos de un modelo.

        :return: listado de todos los usuarios.
        :rtype: list of Model
        """
        return self.session.query(self.model).all()

    def insert(self, obj):
        """
        Dar de alta un objeto de un modelo.

        :type obj: Model
        :rtype: Model
        """
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, obj):
        """
        Guardar un objeto de un modelo con sus datos modificados.

        :type obj: Model
        :rtype: Model
        """
        self.session.commit()
        return obj

    def delete(self, object_id):
        """
        Borrar un objeto de un modelo dado su id.

        :type object_id: int
        :rtype: bool
        """
        if self.session.query(self.model).filter(self.model.id == object_id).delete():
            self.session.commit()
            return True
        return False


class UserData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = User

    def get_by_email(self, email):
        """
        Recuperar un usuario dado su email.

        :type email: str
        :rtype: User | None
        """
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username):
        """
        Recuperar un usuario dado su nombre de usuario.

        :type username: str
        :rtype: User | None
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_by_username_email(self, username_email):
        """
        Recuperar un usuario dado su nombre de usuario o e-mail.

        :type username_email: str
        :rtype: User | None
        """
        user = self.get_by_username(username_email)
        if user is None:
            user = self.get_by_email(username_email)
        return user


class LocationData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = Location

    def get_all_by_user_id(self, user_id):
        """
        Recuperar todas las ubicaciones pertenecientes a un usuario dado su id.

        :type user_id: int
        :rtype: list of Location
        """
        return self.session.query(Location).filter(Location.owner_id == user_id).all()


class CategoryData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = Category

    def get_general_categories(self):
        """
        Recuperar las categorías generales, no creadas por ningún usuario particular.

        :rtype: list of Category
        """
        self.session.query(Category).filter(Category.creator_id is None).all()

    def get_all_by_user_id(self, user_id):
        """
        Recuperar todas las categorías creadas por un usuario dado su id.

        :type user_id: int
        :rtype: list of Category
        """
        return self.session.query(Category).filter(Category.creator_id == user_id).all()


class ItemData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = Item

    def get_all_by_user_id(self, user_id):
        """
        Recuperar todos los ítems pertenecientes a un usuario dado su id.

        :type user_id: int
        :rtype: list of Item
        """
        return self.session.query(Item).filter(Item.owner_id == user_id).all()

    def get_all_by_location_id(self, location_id):
        """
        Recuperar todos los ítems que están en una ubicación dado su id.

        :type location_id: int
        :rtype: list of Item
        """
        return self.session.query(Item).filter(Item.location_id == location_id).all()


class UsageData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = Usage

    def get_all_by_item_id(self, item_id):
        """
        Recuperar todas las utilizaciones de un item dado su id.

        :type item_id: int
        :rtype: list of Usage
        """
        return self.session.query(Usage).filter(Usage.item_id == item_id).all()
