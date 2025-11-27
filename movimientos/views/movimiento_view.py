from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from movimientos.models import Movimiento
from movimientos.serializers import MovimientoSerializer
from port_control.permissions import MovimientoPermission


class MovimientoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Movimientos de Contenedores
    
    Permisos:
    - CRUD: ADMIN, CAPITAN_PUERTO, OPERADOR_TERMINAL
    - Leer: INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    permission_classes = [MovimientoPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contenedor', 'tipo_movimiento', 'zona_origen', 'zona_destino', 'operador']
    search_fields = ['tipo_movimiento', 'contenedor__codigo_contenedor']
    ordering_fields = ['fecha_hora', 'tipo_movimiento']
    ordering = ['-fecha_hora']
