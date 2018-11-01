from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from personal_inventory.data.models import Base, User, Location, Item

engine = None
db_session = None
configured = False


def configure(data_conf):
    """
    Configurar la capa de datos con la config de la db (url, etc).

    :type data_conf: DataConf
    """
    global engine
    engine = engine_from_config(data_conf.DB_CONF)
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
            raise Exception('Data layer not configured')
        self.session = db_session(autoflush=False)
        self.model = None  # reemplazar en las subclases

    def get_by_id(self, object_id):
        """
        Recuperar un objeto del modelo dado su id.

        :type object_id: int
        :rtype: Model
        """
        return self.session.query(self.model).filter(self.model.id == object_id).first()

    def get_all(self):
        """
        Recuperar todos los objetos del modelo.

        :rtype: list of Model
        """
        return self.session.query(self.model).all()

    def insert(self, obj):
        """
        Dar de alta un objeto del modelo.

        :type obj: Model
        :rtype: Model
        """
        self.session.add(obj)
        self.session.commit()
        return obj

    def update(self, obj):
        """
        Guardar un objeto del modelo con sus datos modificados.

        :type obj: Model
        :rtype: Model
        """
        self.session.commit()
        return obj

    def delete(self, object_id):
        """
        Borrar un objeto del modelo dado su id.

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

    def get_all_by_user(self, user):
        """
        Recuperar todas las ubicaciones pertenecientes a un usuario.

        :type user: User
        :rtype: list of Location
        """
        return self.session.query(Location).filter(Location.owner_id == user.id).all()


class ItemData(ObjectData):

    def __init__(self):
        super().__init__()
        self.model = Item

    def get_all_by_user(self, user):
        """
        Recuperar todos los ítems pertenecientes a un usuario.

        :type user: User
        :rtype: list of Item
        """
        return self.session.query(Item).filter(Item.owner_id == user.id).all()

    def get_all_by_location(self, location):
        """
        Recuperar todos los ítems que están en una ubicación.

        :type location: Location
        :rtype: list of Item
        """
        return self.session.query(Item).filter(Item.location_id == location.id).all()
