from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from personal_inventory.model import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(50), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(30))
    items = relationship('Item')
    locations = relationship('Location')
