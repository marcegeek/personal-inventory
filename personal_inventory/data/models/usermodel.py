from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

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
    items = relationship('ItemModel', backref='owner', viewonly=True, bake_queries=False)
    locations = relationship('LocationModel', backref='owner', viewonly=True, bake_queries=False)
