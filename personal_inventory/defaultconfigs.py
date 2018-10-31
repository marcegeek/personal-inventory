class DataConfig:
    DB_CONF = {'sqlalchemy.url': 'sqlite://'}


class PersistentDataConfig(DataConfig):
    DB_CONF = {'sqlalchemy.url': 'sqlite:///db.sqlite'}


class MemoryDataConfig(DataConfig):
    pass


class FlaskConfig:
    TESTING = False
    SECRET_KEY = 'change this'
