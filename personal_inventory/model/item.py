from sqlalchemy import Column, Integer, ForeignKey, String, case, text
from sqlalchemy.orm import relationship

from personal_inventory.model import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(50))
    location_id = Column(Integer, ForeignKey('locations.id'))
    usages = relationship('Usage')
    quantity = Column(Integer)

    __mapper_args__ = {
        'polymorphic_on': case([
            (text('quantity is null'), 'item')
        ], else_='nonatomicitem'),
        'polymorphic_identity': 'item'
    }


class NonAtomicItem(Item):
    __mapper_args__ = {
        'polymorphic_identity': 'nonatomicitem'
    }
