from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from barcos.models import Barco
from barcos.serializers import BarcoSerializer
from port_control.permissions import BarcoPermission


class BarcoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Barcos
    
    Permisos:
    - CRUD: ADMIN, CAPITAN_PUERTO, AGENTE_NAVIERO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, VIGILANTE
    """
    queryset = Barco.objects.all()
    serializer_class = BarcoSerializer
    permission_classes = [BarcoPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo', 'bandera', 'empresa_operadora']
    search_fields = ['nombre', 'bandera', 'tipo', 'empresa_operadora']
    ordering_fields = ['nombre', 'fecha_llegada', 'fecha_salida']
    ordering = ['-fecha_llegada']
