"""
Modelos para el sistema de ubicación en tiempo real de buques.
Estos modelos se almacenan en MongoDB.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from port_control.mongodb import get_mongo_db
from bson import ObjectId
import json


class UbicacionBuque:
    """
    Modelo para almacenar la ubicación de un buque en tiempo real.
    Se almacena en MongoDB con índices geoespaciales.
    """
    
    COLLECTION_NAME = 'ubicaciones_buques'
    
    def __init__(self, barco_id: str, latitud: float, longitud: float, 
                 velocidad: float = 0.0, rumbo: float = 0.0, 
                 timestamp: Optional[datetime] = None, 
                 estado: str = 'en_transito', metadata: Optional[Dict] = None):
        """
        Inicializa una ubicación de buque.
        
        Args:
            barco_id: UUID del barco (desde PostgreSQL)
            latitud: Latitud en grados decimales
            longitud: Longitud en grados decimales
            velocidad: Velocidad en nudos (default: 0.0)
            rumbo: Rumbo en grados (0-360, default: 0.0)
            timestamp: Fecha y hora de la ubicación (default: ahora)
            estado: Estado del buque (en_transito, atracado, fondeado, etc.)
            metadata: Información adicional (altura, calado, etc.)
        """
        self.barco_id = barco_id
        self.latitud = latitud
        self.longitud = longitud
        self.velocidad = velocidad
        self.rumbo = rumbo
        self.timestamp = timestamp or datetime.utcnow()
        self.estado = estado
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la ubicación a un diccionario para MongoDB."""
        return {
            'barco_id': self.barco_id,
            'ubicacion': {
                'type': 'Point',
                'coordinates': [self.longitud, self.latitud]  # MongoDB usa [long, lat]
            },
            'velocidad': self.velocidad,
            'rumbo': self.rumbo,
            'timestamp': self.timestamp,
            'estado': self.estado,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UbicacionBuque':
        """Crea una instancia desde un diccionario de MongoDB."""
        ubicacion = data.get('ubicacion', {})
        coords = ubicacion.get('coordinates', [0, 0])
        
        return cls(
            barco_id=data.get('barco_id'),
            latitud=coords[1],
            longitud=coords[0],
            velocidad=data.get('velocidad', 0.0),
            rumbo=data.get('rumbo', 0.0),
            timestamp=data.get('timestamp'),
            estado=data.get('estado', 'en_transito'),
            metadata=data.get('metadata', {})
        )
    
    @classmethod
    def get_collection(cls):
        """Obtiene la colección de MongoDB."""
        db = get_mongo_db()
        return db[cls.COLLECTION_NAME]
    
    @classmethod
    def create_indexes(cls):
        """
        Crea los índices necesarios en la colección.
        - Índice geoespacial 2dsphere para búsquedas por ubicación
        - Índice en barco_id para búsquedas por barco
        - Índice en timestamp para búsquedas temporales
        """
        collection = cls.get_collection()
        
        # Índice geoespacial
        collection.create_index([("ubicacion", "2dsphere")])
        
        # Índice en barco_id
        collection.create_index([("barco_id", 1)])
        
        # Índice en timestamp (descendente para obtener las más recientes primero)
        collection.create_index([("timestamp", -1)])
        
        # Índice compuesto para búsquedas por barco y tiempo
        collection.create_index([("barco_id", 1), ("timestamp", -1)])
    
    def save(self) -> str:
        """
        Guarda la ubicación en MongoDB.
        Retorna el _id del documento insertado.
        """
        collection = self.get_collection()
        data = self.to_dict()
        result = collection.insert_one(data)
        return str(result.inserted_id)
    
    @classmethod
    def get_ultima_ubicacion(cls, barco_id: str) -> Optional['UbicacionBuque']:
        """
        Obtiene la última ubicación registrada de un barco.
        """
        collection = cls.get_collection()
        doc = collection.find_one(
            {'barco_id': barco_id},
            sort=[('timestamp', -1)]
        )
        
        if doc:
            doc['_id'] = str(doc['_id'])  # Convertir ObjectId a string
            return cls.from_dict(doc)
        return None
    
    @classmethod
    def get_ubicaciones_por_rango_tiempo(cls, barco_id: str, 
                                         inicio: datetime, 
                                         fin: datetime) -> list:
        """
        Obtiene todas las ubicaciones de un barco en un rango de tiempo.
        """
        collection = cls.get_collection()
        docs = collection.find({
            'barco_id': barco_id,
            'timestamp': {'$gte': inicio, '$lte': fin}
        }).sort('timestamp', 1)
        
        ubicaciones = []
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            ubicaciones.append(cls.from_dict(doc))
        
        return ubicaciones
    
    @classmethod
    def get_buques_cercanos(cls, latitud: float, longitud: float, 
                           radio_km: float = 10.0) -> list:
        """
        Obtiene todos los buques dentro de un radio determinado.
        
        Args:
            latitud: Latitud del punto central
            longitud: Longitud del punto central
            radio_km: Radio en kilómetros (default: 10 km)
        
        Returns:
            Lista de ubicaciones de buques cercanos
        """
        collection = cls.get_collection()
        
        # Convertir radio de km a metros (MongoDB usa metros)
        radio_metros = radio_km * 1000
        
        # Búsqueda geoespacial
        docs = collection.find({
            'ubicacion': {
                '$near': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': [longitud, latitud]
                    },
                    '$maxDistance': radio_metros
                }
            }
        })
        
        ubicaciones = []
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            ubicaciones.append(cls.from_dict(doc))
        
        return ubicaciones
    
    @classmethod
    def get_todas_ubicaciones_actuales(cls) -> list:
        """
        Obtiene la última ubicación de cada barco.
        """
        collection = cls.get_collection()
        
        # Agregación para obtener la última ubicación de cada barco
        pipeline = [
            {'$sort': {'barco_id': 1, 'timestamp': -1}},
            {'$group': {
                '_id': '$barco_id',
                'ultima_ubicacion': {'$first': '$$ROOT'}
            }},
            {'$replaceRoot': {'newRoot': '$ultima_ubicacion'}}
        ]
        
        docs = collection.aggregate(pipeline)
        
        ubicaciones = []
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            ubicaciones.append(cls.from_dict(doc))
        
        return ubicaciones

