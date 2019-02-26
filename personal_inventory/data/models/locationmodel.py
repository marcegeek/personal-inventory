from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from personal_inventory.data.models import Base


class LocationModel(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(50), nullable=False)
    items = relationship('ItemModel', backref='location', viewonly=True, bake_queries=False)

    def __eq__(self, other):
        o1 = (self.id, self.owner_id, self.description)
        o2 = (other.id, other.owner_id, other.description)
        return o1 == o2
