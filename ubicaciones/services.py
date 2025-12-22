"""
Servicio para simular ubicaciones en tiempo real de buques.
"""
import asyncio
import random
import math
from datetime import datetime, timedelta
from typing import List, Optional
from threading import Thread
import time

from ubicaciones.models import UbicacionBuque
from barcos.models import Barco
import logging

logger = logging.getLogger(__name__)


class SimuladorUbicaciones:
    """
    Servicio para simular el movimiento de buques en tiempo real.
    """
    
    def __init__(self):
        self.activo = False
        self.hilo = None
        self.intervalo_segundos = 30  # Actualizar cada 30 segundos por defecto
    
    def iniciar(self, intervalo_segundos: int = 30):
        """
        Inicia la simulación de ubicaciones.
        
        Args:
            intervalo_segundos: Intervalo entre actualizaciones (default: 30)
        """
        if self.activo:
            logger.warning("La simulación ya está activa")
            return
        
        self.intervalo_segundos = intervalo_segundos
        self.activo = True
        self.hilo = Thread(target=self._simular_loop, daemon=True)
        self.hilo.start()
        logger.info(f"Simulación de ubicaciones iniciada (intervalo: {intervalo_segundos}s)")
    
    def detener(self):
        """Detiene la simulación de ubicaciones."""
        self.activo = False
        if self.hilo:
            self.hilo.join(timeout=5)
        logger.info("Simulación de ubicaciones detenida")
    
    def _simular_loop(self):
        """Loop principal de simulación."""
        while self.activo:
            try:
                self._actualizar_ubicaciones()
                time.sleep(self.intervalo_segundos)
            except Exception as e:
                logger.error(f"Error en simulación: {e}")
                time.sleep(self.intervalo_segundos)
    
    def _actualizar_ubicaciones(self):
        """Actualiza las ubicaciones de todos los barcos activos."""
        try:
            # Obtener todos los barcos desde PostgreSQL
            barcos = Barco.objects.all()
            
            for barco in barcos:
                try:
                    # Obtener última ubicación
                    ultima_ubicacion = UbicacionBuque.get_ultima_ubicacion(str(barco.id))
                    
                    if ultima_ubicacion:
                        # Calcular nueva ubicación basada en la anterior
                        nueva_ubicacion = self._calcular_nueva_ubicacion(ultima_ubicacion)
                    else:
                        # Primera ubicación: posición inicial aleatoria cerca del puerto
                        nueva_ubicacion = self._generar_ubicacion_inicial(barco)
                    
                    # Guardar nueva ubicación
                    nueva_ubicacion.save()
                    logger.debug(f"Ubicación actualizada para barco {barco.nombre}")
                    
                except Exception as e:
                    logger.error(f"Error al actualizar ubicación del barco {barco.id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error al obtener barcos: {e}")
    
    def _calcular_nueva_ubicacion(self, ubicacion_anterior: UbicacionBuque) -> UbicacionBuque:
        """
        Calcula una nueva ubicación basada en la anterior.
        Simula movimiento realista de un buque.
        """
        # Coordenadas del puerto de Panamá (ejemplo)
        PUERTO_LAT = 8.9824
        PUERTO_LON = -79.5199
        
        # Si está cerca del puerto, puede estar atracado
        distancia_al_puerto = self._calcular_distancia(
            ubicacion_anterior.latitud, ubicacion_anterior.longitud,
            PUERTO_LAT, PUERTO_LON
        )
        
        # Determinar estado y movimiento
        if distancia_al_puerto < 0.5:  # Menos de 0.5 km del puerto
            # Puede estar atracado o en espera
            estado = random.choice(['atracado', 'en_espera', 'atracado'])
            velocidad = random.uniform(0, 2)  # Muy lento
        else:
            estado = 'en_transito'
            velocidad = random.uniform(5, 20)  # 5-20 nudos
        
        # Calcular nueva posición
        # 1 nudo ≈ 1.852 km/h
        # Convertir a grados (aproximado: 1 grado ≈ 111 km)
        velocidad_kmh = velocidad * 1.852
        distancia_km = (velocidad_kmh * self.intervalo_segundos) / 3600
        
        # Rumbo (puede variar ligeramente)
        rumbo = ubicacion_anterior.rumbo + random.uniform(-5, 5)
        if rumbo < 0:
            rumbo += 360
        elif rumbo >= 360:
            rumbo -= 360
        
        # Convertir rumbo a radianes
        rumbo_rad = math.radians(rumbo)
        
        # Calcular desplazamiento
        # lat: 1 grado ≈ 111 km
        # lon: 1 grado ≈ 111 km * cos(lat)
        delta_lat = (distancia_km * math.cos(rumbo_rad)) / 111
        delta_lon = (distancia_km * math.sin(rumbo_rad)) / (111 * math.cos(math.radians(ubicacion_anterior.latitud)))
        
        nueva_lat = ubicacion_anterior.latitud + delta_lat
        nueva_lon = ubicacion_anterior.longitud + delta_lon
        
        # Asegurar que esté en rangos válidos
        nueva_lat = max(-90, min(90, nueva_lat))
        nueva_lon = max(-180, min(180, nueva_lon))
        
        return UbicacionBuque(
            barco_id=ubicacion_anterior.barco_id,
            latitud=nueva_lat,
            longitud=nueva_lon,
            velocidad=velocidad,
            rumbo=rumbo,
            estado=estado,
            metadata={
                'distancia_puerto_km': round(distancia_al_puerto, 2),
                'simulado': True
            }
        )
    
    def _generar_ubicacion_inicial(self, barco: Barco) -> UbicacionBuque:
        """
        Genera una ubicación inicial para un barco.
        """
        # Coordenadas del puerto de Panamá (ejemplo)
        PUERTO_LAT = 8.9824
        PUERTO_LON = -79.5199
        
        # Generar posición aleatoria cerca del puerto (dentro de 50 km)
        radio_km = random.uniform(5, 50)
        angulo = random.uniform(0, 2 * math.pi)
        
        # Convertir a grados
        delta_lat = (radio_km * math.cos(angulo)) / 111
        delta_lon = (radio_km * math.sin(angulo)) / (111 * math.cos(math.radians(PUERTO_LAT)))
        
        latitud = PUERTO_LAT + delta_lat
        longitud = PUERTO_LON + delta_lon
        
        # Rumbo inicial aleatorio
        rumbo = random.uniform(0, 360)
        velocidad = random.uniform(5, 15)
        
        return UbicacionBuque(
            barco_id=str(barco.id),
            latitud=latitud,
            longitud=longitud,
            velocidad=velocidad,
            rumbo=rumbo,
            estado='en_transito',
            metadata={
                'inicial': True,
                'simulado': True
            }
        )
    
    def _calcular_distancia(self, lat1: float, lon1: float, 
                           lat2: float, lon2: float) -> float:
        """
        Calcula la distancia entre dos puntos en kilómetros usando la fórmula de Haversine.
        """
        R = 6371  # Radio de la Tierra en km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = R * c
        
        return distancia


# Instancia global del simulador
simulador = SimuladorUbicaciones()

