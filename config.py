from enum import Enum

from personal_inventory.defaultconfigs import FlaskConfig, PersistentDataConfig, MemoryDataConfig


class Environment(Enum):
    PRODUCTION = 'PROD'
    TESTING = 'TESTING'
    DEVELOPMENT = 'DEV'


class ProductionFlaskConfig(FlaskConfig):
    SECRET_KEY = 'real key here'


class TestingFlaskConfig(FlaskConfig):
    TESTING = True
    SECRET_KEY = 'real key here'


class DevelopmentFlaskConfig(TestingFlaskConfig):
    DEBUG = True
    SECRET_KEY = 'real key here'


ENVIRONMENT = Environment.DEVELOPMENT
DATA_IS_PERSISTENT = True


def get_configs():
    if ENVIRONMENT == Environment.PRODUCTION:
        return {'data': PersistentDataConfig, 'flask': ProductionFlaskConfig}
    if ENVIRONMENT == Environment.TESTING:
        data = MemoryDataConfig
        if DATA_IS_PERSISTENT:
            data = PersistentDataConfig
        return {'data': data, 'flask': TestingFlaskConfig}
    if ENVIRONMENT == Environment.DEVELOPMENT:
        data = MemoryDataConfig
        if DATA_IS_PERSISTENT:
            data = PersistentDataConfig
        return {'data': data, 'flask': DevelopmentFlaskConfig}
    else:
        raise Exception('bad environment configuration')
