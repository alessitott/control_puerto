"""
Módulo de conexión a MongoDB para el sistema de ubicación en tiempo real de buques.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Cliente MongoDB global
_mongo_client = None
_mongo_db = None


def get_mongo_client():
    """
    Obtiene o crea el cliente de MongoDB.
    Utiliza variables de entorno para la configuración.
    """
    global _mongo_client
    
    if _mongo_client is None:
        try:
            # Obtener configuración de variables de entorno
            mongo_host = os.getenv('MONGO_HOST', 'localhost')
            mongo_port = int(os.getenv('MONGO_PORT', '27017'))
            mongo_username = os.getenv('MONGO_USERNAME', '')
            mongo_password = os.getenv('MONGO_PASSWORD', '')
            mongo_database = os.getenv('MONGO_DATABASE', 'control_puerto')
            mongo_auth_source = os.getenv('MONGO_AUTH_SOURCE', 'admin')
            
            # Construir URI de conexión
            if mongo_username and mongo_password:
                # Conexión con autenticación
                mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_database}?authSource={mongo_auth_source}"
            else:
                # Conexión sin autenticación (desarrollo local)
                mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/{mongo_database}"
            
            # También soportar MongoDB Atlas (URI completa)
            mongo_uri_env = os.getenv('MONGO_URI')
            if mongo_uri_env:
                mongo_uri = mongo_uri_env
            
            # Crear cliente
            _mongo_client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,  # Timeout de 5 segundos
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Verificar conexión
            _mongo_client.admin.command('ping')
            logger.info(f"Conexión exitosa a MongoDB en {mongo_host}:{mongo_port}")
            
        except ConnectionFailure as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            raise
        except ConfigurationError as e:
            logger.error(f"Error de configuración de MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al conectar a MongoDB: {e}")
            raise
    
    return _mongo_client


def get_mongo_db():
    """
    Obtiene la base de datos de MongoDB.
    """
    global _mongo_db
    
    if _mongo_db is None:
        client = get_mongo_client()
        mongo_database = os.getenv('MONGO_DATABASE', 'control_puerto')
        _mongo_db = client[mongo_database]
    
    return _mongo_db


def close_mongo_connection():
    """
    Cierra la conexión a MongoDB.
    """
    global _mongo_client, _mongo_db
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _mongo_db = None
        logger.info("Conexión a MongoDB cerrada")


def test_connection():
    """
    Prueba la conexión a MongoDB.
    Retorna True si la conexión es exitosa, False en caso contrario.
    """
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Error al probar conexión: {e}")
        return False

