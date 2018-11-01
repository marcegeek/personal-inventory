from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(30), nullable=False)


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parent_loc_id = Column(Integer, ForeignKey('locations.id'))
    description = Column(String(50), nullable=False)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(50), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    quantity = Column(Integer)


class Usage(Base):
    __tablename__ = 'usages'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
