from sqlalchemy import Column, Integer, ForeignKey, Date

from personal_inventory.data.models import Base


class UsageModel(Base):
    __tablename__ = 'usages'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
