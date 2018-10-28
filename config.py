"""
Módulo de configuración.

Maneja las configuraciones para los entornos de producción
y pruebas.
"""

PRODUCTION = 'prod'
TESTING = 'test'

DB_CONFIGS = {
    'prod': {'db.url': 'sqlite:///db.sqlite'},
    'test': {'db.url': 'sqlite://'}
}

env = PRODUCTION


def getdbconf():
    return DB_CONFIGS[env]
