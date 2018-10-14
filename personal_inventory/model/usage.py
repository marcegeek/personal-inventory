from sqlalchemy import Column, Integer, ForeignKey, Date

from personal_inventory.model import Base


class Usage(Base):
    __tablename__ = 'usages'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    start_date = Column(Date)
    end_date = Column(Date)
