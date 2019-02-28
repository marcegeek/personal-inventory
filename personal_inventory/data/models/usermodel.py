from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import object_session

from personal_inventory.data.models import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    language = Column(String(5))

    @property
    def items(self):
        from personal_inventory.data import ItemModel
        return object_session(self).query(ItemModel).filter(ItemModel.owner_id == self.id).all()

    @property
    def locations(self):
        from personal_inventory.data import LocationModel
        return object_session(self).query(LocationModel).filter(LocationModel.owner_id == self.id).all()

    def __eq__(self, other):
        o1 = (self.id, self.firstname, self.lastname, self.email,
              self.username, self.password, self.language)
        o2 = (other.id, other.firstname, other.lastname, other.email,
              other.username, other.password, other.language)
        return o1 == o2
