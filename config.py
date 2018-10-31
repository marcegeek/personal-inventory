from personal_inventory.defaultconfigs import FlaskConfig


class ProductionFlaskConfig(FlaskConfig):
    SECRET_KEY = 'real key here'


class TestingFlaskConfig(FlaskConfig):
    TESTING = True
    SECRET_KEY = 'real key here'


class DevelopmentFlaskConfig(FlaskConfig):
    DEBUG = True
    SECRET_KEY = 'real key here'
