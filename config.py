"""
Módulo de configuración.

Maneja las configuraciones para los entornos de producción
y pruebas.
"""

production = 'prod'
testing = 'test'

db_configs = {
    'prod': {'db.url': 'sqlite:///db.sqlite'},
    'test': {'db.url': 'sqlite://'}
}

env = production


def getdbconf():
    return db_configs[env]
