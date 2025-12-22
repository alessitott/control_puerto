"""
Comando de gestión para inicializar los índices de MongoDB.
Ejecutar: python manage.py init_mongodb
"""
from django.core.management.base import BaseCommand
from ubicaciones.models import UbicacionBuque
from port_control.mongodb import test_connection
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Inicializa los índices de MongoDB para el sistema de ubicaciones'

    def handle(self, *args, **options):
        self.stdout.write('Inicializando índices de MongoDB...')
        
        # Probar conexión
        if not test_connection():
            self.stdout.write(
                self.style.ERROR('❌ Error: No se pudo conectar a MongoDB')
            )
            self.stdout.write(
                self.style.WARNING(
                    'Verifica las variables de entorno:\n'
                    '  - MONGO_HOST\n'
                    '  - MONGO_PORT\n'
                    '  - MONGO_DATABASE\n'
                    '  - MONGO_USERNAME (opcional)\n'
                    '  - MONGO_PASSWORD (opcional)\n'
                    '  - MONGO_URI (opcional, para MongoDB Atlas)'
                )
            )
            return
        
        try:
            # Crear índices
            UbicacionBuque.create_indexes()
            
            self.stdout.write(
                self.style.SUCCESS('✅ Índices de MongoDB creados exitosamente')
            )
            self.stdout.write('Índices creados:')
            self.stdout.write('  - Geoespacial 2dsphere en "ubicacion"')
            self.stdout.write('  - Índice en "barco_id"')
            self.stdout.write('  - Índice en "timestamp"')
            self.stdout.write('  - Índice compuesto (barco_id, timestamp)')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear índices: {e}')
            )

