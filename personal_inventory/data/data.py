from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.orm import sessionmaker

from personal_inventory.data.models import Base, User

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


class UserData(ObjectData):

    def get_by_id(self, user_id):
        """
        Recuperar un usuario dado su id.

        :type user_id: int
        :param user_id: id del usuario a recuperar
        :return: usuario con ese id o None si no existe
        :rtype: User | None
        """
        return self.session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email):
        """
        Recuperar un usuario dado su email.

        :type email: str
        :param email: email del usuario a recuperar
        :return: usuario con ese email o None si no existe
        :rtype: User | None
        """
        return self.session.query(User).filter(User.email == email).first()

    def get_by_username(self, username):
        """
        Recuperar un usuario dado su nombre de usuario.

        :type username: str
        :param username: nombre de usuario del usuario a recuperar
        :return: usuario con ese email o None si no existe
        :rtype: User | None
        """
        return self.session.query(User).filter(User.username == username).first()

    def get_all(self):
        """
        Recuperar todos los usuarios.

        :return: listado de todos los usuarios.
        :rtype: list of User
        """
        return self.session.query(User).all()

    def insert(self, user):
        """
        Dar de alta un usuario.

        :type user: User
        :param user: el usuario a dar de alta
        :return: el usuario dado de alta
        :rtype: User
        """
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user):
        """
        Guardar un usuario con sus datos modificados.

        :type user: User
        :param user: el usuario con datos modificados a guardar
        :return: el usuario modificado
        :rtype: User
        """
        self.session.commit()
        return user

    def delete(self, user_id):
        """
        Borrar un usuario dado su id.

        :type user_id: int
        :param user_id: id del usuario a eliminar
        :return: True si el borrado fue exitoso
        :rtype: bool
        """
        if self.session.query(User).filter(User.id == user_id).delete():
            self.session.commit()
            return True
        return False


class LocationData(ObjectData):

    def get_by_id(self, location_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all(self):
        pass

    def insert(self, location):
        pass

    def update(self, location):
        pass

    def delete(self, location_id):
        pass


class CategoryData(ObjectData):

    def get_by_id(self, category_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all(self):
        pass

    def insert(self, category):
        pass

    def update(self, category):
        pass

    def delete(self, category_id):
        pass


class ItemData(ObjectData):

    def get_by_id(self, item_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all_by_location(self, location):
        pass

    def get_all(self):
        pass

    def insert(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, item_id):
        pass


class UsageData(ObjectData):

    def get_by_id(self, usage_id):
        pass

    def get_all_by_item(self):
        pass

    def get_all(self):
        pass

    def insert(self, usage):
        pass

    def update(self, usage):
        pass

    def delete(self, usage_id):
        pass
