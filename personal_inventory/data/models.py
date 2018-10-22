from sqlalchemy import Column, Integer, String, ForeignKey, case, text, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    #parent_loc_id = Column(Integer, ForeignKey('locations.id'))
    description = Column(String(50))
    #sublocations = relationship('Location', backref='parent_location')
    items = relationship('Item', backref='location')


items_categories_association = Table('items_categories', Base.metadata,
                                     Column('item_id', Integer, ForeignKey('items.id')),
                                     Column('category_id', Integer, ForeignKey('categories.id')))


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(50))
    location_id = Column(Integer, ForeignKey('locations.id'))
    categories = relationship('Category', secondary=items_categories_association)
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


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    description = Column(String(50))
    creator_id = Column(Integer, ForeignKey('users.id'))


class Usage(Base):
    __tablename__ = 'usages'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    start_date = Column(Date)
    end_date = Column(Date)
