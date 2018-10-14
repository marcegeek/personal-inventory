from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from personal_inventory.model import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(50))
    parent_loc = Column(Integer, ForeignKey('locations.id'))
    sublocations = relationship('Location')
    items = relationship('Item', backref='location')
