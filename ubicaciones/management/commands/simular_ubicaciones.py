"""
Comando para simular el envío de ubicaciones de barcos a MongoDB.
Ejecutar: python manage.py simular_ubicaciones
"""
from django.core.management.base import BaseCommand
from ubicaciones.models import UbicacionBuque
from barcos.models import Barco
import random
import math
from datetime import datetime
import time


class Command(BaseCommand):
    help = 'Simula el envío de ubicaciones de barcos a MongoDB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--intervalo',
            type=int,
            default=30,
            help='Intervalo en segundos entre actualizaciones (default: 30)',
        )
        parser.add_argument(
            '--veces',
            type=int,
            default=10,
            help='Número de veces que se enviarán ubicaciones (default: 10)',
        )
        parser.add_argument(
            '--continuo',
            action='store_true',
            help='Ejecutar de forma continua hasta que se detenga (Ctrl+C)',
        )

    def handle(self, *args, **options):
        intervalo = options['intervalo']
        veces = options['veces']
        continuo = options['continuo']

        self.stdout.write(
            self.style.SUCCESS(f'🚢 Iniciando simulación de ubicaciones...')
        )
        self.stdout.write(f'Intervalo: {intervalo} segundos')
        
        if continuo:
            self.stdout.write('Modo: Continuo (Ctrl+C para detener)')
        else:
            self.stdout.write(f'Modo: {veces} iteraciones')

        # Coordenadas del puerto de Panamá (ejemplo)
        PUERTO_LAT = 8.9824
        PUERTO_LON = -79.5199

        try:
            iteracion = 0
            while True:
                iteracion += 1
                
                if not continuo and iteracion > veces:
                    break

                self.stdout.write(f'\n--- Iteración {iteracion} ---')
                
                # Obtener todos los barcos
                barcos = Barco.objects.all()
                
                if not barcos.exists():
                    self.stdout.write(
                        self.style.WARNING('⚠️  No hay barcos registrados. Crea algunos barcos primero.')
                    )
                    break

                ubicaciones_enviadas = 0

                for barco in barcos:
                    try:
                        # Obtener última ubicación
                        ultima_ubicacion = UbicacionBuque.get_ultima_ubicacion(str(barco.id))
                        
                        if ultima_ubicacion:
                            # Calcular nueva ubicación
                            nueva_ubicacion = self._calcular_nueva_ubicacion(
                                ultima_ubicacion, PUERTO_LAT, PUERTO_LON
                            )
                        else:
                            # Primera ubicación
                            nueva_ubicacion = self._generar_ubicacion_inicial(
                                barco, PUERTO_LAT, PUERTO_LON
                            )
                        
                        # Guardar en MongoDB
                        ubicacion_id = nueva_ubicacion.save()
                        ubicaciones_enviadas += 1
                        
                        self.stdout.write(
                            f'✅ {barco.nombre}: '
                            f'Lat {nueva_ubicacion.latitud:.4f}, '
                            f'Lon {nueva_ubicacion.longitud:.4f}, '
                            f'Vel {nueva_ubicacion.velocidad:.1f} nudos, '
                            f'Estado: {nueva_ubicacion.estado}'
                        )
                        
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Error con barco {barco.nombre}: {e}')
                        )
                        continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✓ {ubicaciones_enviadas} ubicaciones enviadas a MongoDB'
                    )
                )

                if not continuo and iteracion < veces:
                    self.stdout.write(f'Esperando {intervalo} segundos...')
                    time.sleep(intervalo)

        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\n\n⚠️  Simulación detenida por el usuario')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error: {e}')
            )

    def _calcular_nueva_ubicacion(self, ubicacion_anterior, puerto_lat, puerto_lon):
        """Calcula una nueva ubicación basada en la anterior."""
        distancia_al_puerto = self._calcular_distancia(
            ubicacion_anterior.latitud, ubicacion_anterior.longitud,
            puerto_lat, puerto_lon
        )

        # Determinar estado y velocidad
        if distancia_al_puerto < 0.5:
            estado = random.choice(['atracado', 'en_espera', 'atracado'])
            velocidad = random.uniform(0, 2)
        else:
            estado = 'en_transito'
            velocidad = random.uniform(5, 20)

        # Calcular nueva posición
        velocidad_kmh = velocidad * 1.852
        distancia_km = (velocidad_kmh * 30) / 3600  # 30 segundos

        # Rumbo con variación
        rumbo = ubicacion_anterior.rumbo + random.uniform(-5, 5)
        if rumbo < 0:
            rumbo += 360
        elif rumbo >= 360:
            rumbo -= 360

        rumbo_rad = math.radians(rumbo)

        # Desplazamiento
        delta_lat = (distancia_km * math.cos(rumbo_rad)) / 111
        delta_lon = (distancia_km * math.sin(rumbo_rad)) / (111 * math.cos(math.radians(ubicacion_anterior.latitud)))

        nueva_lat = ubicacion_anterior.latitud + delta_lat
        nueva_lon = ubicacion_anterior.longitud + delta_lon

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
                'simulado': True,
                'timestamp_envio': datetime.utcnow().isoformat()
            }
        )

    def _generar_ubicacion_inicial(self, barco, puerto_lat, puerto_lon):
        """Genera una ubicación inicial para un barco."""
        radio_km = random.uniform(5, 50)
        angulo = random.uniform(0, 2 * math.pi)

        delta_lat = (radio_km * math.cos(angulo)) / 111
        delta_lon = (radio_km * math.sin(angulo)) / (111 * math.cos(math.radians(puerto_lat)))

        latitud = puerto_lat + delta_lat
        longitud = puerto_lon + delta_lon

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
                'simulado': True,
                'timestamp_envio': datetime.utcnow().isoformat()
            }
        )

    def _calcular_distancia(self, lat1, lon1, lat2, lon2):
        """Calcula distancia en km usando fórmula de Haversine."""
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

