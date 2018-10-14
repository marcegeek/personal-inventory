from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from personal_inventory.model import Base

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.bind = engine
db_session = sessionmaker()
Base.metadata.create_all(engine)


def make_session():
    return db_session(autoflush=False)
