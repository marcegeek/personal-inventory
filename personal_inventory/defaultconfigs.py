from sqlalchemy.pool import StaticPool


class DataConfig:
    DB_CONF = {
        'sqlalchemy.url': 'sqlite://',
        'sqlalchemy.connect_args': {'check_same_thread': False},
        'sqlalchemy.poolclass': StaticPool
    }


class PersistentDataConfig(DataConfig):
    DB_CONF = {
        'sqlalchemy.url': 'sqlite:///db.sqlite',
        'sqlalchemy.connect_args': {'check_same_thread': False}
    }


class MemoryDataConfig(DataConfig):
    pass


class FlaskConfig:
    TESTING = False
    SECRET_KEY = 'change this'
