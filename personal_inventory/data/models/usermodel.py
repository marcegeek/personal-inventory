from sqlalchemy import Column, Integer, String

from personal_inventory.data.models import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
