import os

from personal_inventory.defaultconfigs import ProductionDataConfig, TestingDataConfig
from personal_inventory.data import data as dal
from personal_inventory.presentation import app

env = os.environ.get('ENV')
if env == 'PROD':
    dal.configure(ProductionDataConfig)
    app.config.from_object('config.ProductionFlaskConfig')
elif env == 'TESTING':
    if os.environ.get('DATA') == 'PROD':
        dal.configure(ProductionDataConfig)
    else:
        dal.configure(TestingDataConfig)
    app.config.from_object('config.TestingFlaskConfig')
elif env == 'DEV':
    if os.environ.get('DATA') == 'PROD':
        dal.configure(ProductionDataConfig)
    else:
        dal.configure(TestingDataConfig)
    app.config.from_object('config.DevelopmentFlaskConfig')
app.run()
