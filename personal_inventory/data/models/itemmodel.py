from sqlalchemy import Column, Integer, ForeignKey, String

from personal_inventory.data.models import Base


class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    quantity = Column(Integer)

    def __eq__(self, other):
        o1 = (self.id, self.owner_id, self.description, self.location_id, self.quantity)
        o2 = (other.id, other.owner_id, other.description, other.location_id, other.quantity)
        return o1 == o2
