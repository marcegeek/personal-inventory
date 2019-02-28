from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import object_session

from personal_inventory.data.models import Base


class LocationModel(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(50), nullable=False)

    @property
    def owner(self):
        from personal_inventory.data import UserModel
        return object_session(self).query(UserModel).filter(UserModel.id == self.owner_id).first()

    @property
    def items(self):
        from personal_inventory.data import ItemModel
        return object_session(self).query(ItemModel).filter(ItemModel.location_id == self.id).all()

    def __eq__(self, other):
        o1 = (self.id, self.owner_id, self.description)
        o2 = (other.id, other.owner_id, other.description)
        return o1 == o2
