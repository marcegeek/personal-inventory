class DataConfig:
    DB_CONF = {'sqlalchemy.url': 'sqlite://'}


class ProductionDataConfig(DataConfig):
    DB_CONF = {'sqlalchemy.url': 'sqlite:///db.sqlite'}


class TestingDataConfig(DataConfig):
    pass


class FlaskConfig:
    TESTING = False
    SECRET_KEY = 'change this'
