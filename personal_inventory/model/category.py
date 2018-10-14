from sqlalchemy import Column, Integer, String, ForeignKey

from personal_inventory.model import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    description = Column(String(50))
    creator_id = Column(Integer, ForeignKey('users.id'))
