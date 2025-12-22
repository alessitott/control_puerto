"""
Serializers para el sistema de ubicación de buques.
"""
from rest_framework import serializers
from datetime import datetime


class UbicacionBuqueSerializer(serializers.Serializer):
    """Serializer para ubicaciones de buques."""
    
    barco_id = serializers.UUIDField()
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)
    velocidad = serializers.FloatField(min_value=0, required=False, default=0.0)
    rumbo = serializers.FloatField(min_value=0, max_value=360, required=False, default=0.0)
    timestamp = serializers.DateTimeField(required=False)
    estado = serializers.ChoiceField(
        choices=['en_transito', 'atracado', 'fondeado', 'en_espera', 'salida'],
        required=False,
        default='en_transito'
    )
    metadata = serializers.DictField(required=False, allow_empty=True, default=dict)
    
    def to_representation(self, instance):
        """Convierte la instancia a formato JSON para la respuesta."""
        if isinstance(instance, dict):
            # Si es un diccionario (desde MongoDB)
            ubicacion = instance.get('ubicacion', {})
            coords = ubicacion.get('coordinates', [0, 0])
            
            return {
                'id': str(instance.get('_id', '')),
                'barco_id': instance.get('barco_id'),
                'latitud': coords[1],
                'longitud': coords[0],
                'velocidad': instance.get('velocidad', 0.0),
                'rumbo': instance.get('rumbo', 0.0),
                'timestamp': instance.get('timestamp'),
                'estado': instance.get('estado', 'en_transito'),
                'metadata': instance.get('metadata', {})
            }
        else:
            # Si es una instancia de UbicacionBuque
            return {
                'barco_id': instance.barco_id,
                'latitud': instance.latitud,
                'longitud': instance.longitud,
                'velocidad': instance.velocidad,
                'rumbo': instance.rumbo,
                'timestamp': instance.timestamp,
                'estado': instance.estado,
                'metadata': instance.metadata
            }


class BusquedaCercanosSerializer(serializers.Serializer):
    """Serializer para búsqueda de buques cercanos."""
    
    latitud = serializers.FloatField(min_value=-90, max_value=90)
    longitud = serializers.FloatField(min_value=-180, max_value=180)
    radio_km = serializers.FloatField(min_value=0.1, max_value=1000, required=False, default=10.0)

