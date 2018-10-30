"""
Módulo de configuración.

Maneja las configuraciones para los entornos de producción
y pruebas y realiza los ajustes necesarios a las capas que correspondan.
"""

from enum import Enum

import personal_inventory.data.data as dal


class Environment(Enum):
    PRODUCTION = 'prod'
    TESTING = 'test'


DB_URLS = {
    Environment.PRODUCTION: 'sqlite:///db.sqlite',
    Environment.TESTING: 'sqlite://'
}

environment, data_environment = None, None


def set_environment(env):
    """
    Establecer el entorno de configuración.

    :type env: Environment
    """
    global environment
    environment = env
    set_data_enviroment(env)
    # TODO setear otras configs


def set_data_enviroment(env):
    """
    Establecer el entorno de configuración sólo para la capa de datos.

    Establecer y re-establecer el entorno de testing resetea la db en memoria.

    :type env: Environment
    """
    global data_environment
    data_environment = env
    dal.configure(DB_URLS[data_environment])
