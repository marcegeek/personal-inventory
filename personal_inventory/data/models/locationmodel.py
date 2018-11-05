from sqlalchemy import Column, Integer, ForeignKey, String

from personal_inventory.data.models import Base


class LocationModel(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(50), nullable=False)
