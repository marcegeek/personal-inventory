from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from personal_inventory.data.models import Base

engine = create_engine('sqlite:///db.sqlite')
Base.metadata.bind = engine
db_session = sessionmaker()
Base.metadata.create_all(engine)


class ObjectData:

    def __init__(self):
        self.session = db_session(autoflush=False)


class UserData(ObjectData):

    def get_by_id(self, user_id):
        pass

    def get_by_email(self, email):
        pass

    def get_by_username(self, username):
        pass

    def get_all(self):
        pass

    def insert(self, user):
        pass

    def update(self, user):
        pass

    def delete(self, user_id):
        pass


class LocationData(ObjectData):

    def get_by_id(self, location_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all(self):
        pass

    def insert(self, location):
        pass

    def update(self, location):
        pass

    def delete(self, location_id):
        pass


class CategoryData(ObjectData):

    def get_by_id(self, category_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all(self):
        pass

    def insert(self, category):
        pass

    def update(self, category):
        pass

    def delete(self, category_id):
        pass


class ItemData(ObjectData):

    def get_by_id(self, item_id):
        pass

    def get_all_by_user(self, user):
        pass

    def get_all_by_location(self, location):
        pass

    def get_all(self):
        pass

    def insert(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, item_id):
        pass


class UsageData(ObjectData):

    def get_by_id(self, usage_id):
        pass

    def get_all_by_item(self):
        pass

    def get_all(self):
        pass

    def insert(self, usage):
        pass

    def update(self, usage):
        pass

    def delete(self, usage_id):
        pass
