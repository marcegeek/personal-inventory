class DataConfig:
    DB_CONF = {
        'sqlalchemy.url': 'sqlite://',
        'sqlalchemy.connect_args': {'check_same_thread': False}
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
