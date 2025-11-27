from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from zonas_puerto.models import ZonaPuerto
from zonas_puerto.serializers import ZonaPuertoSerializer
from port_control.permissions import ZonaPuertoPermission


class ZonaPuertoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Zonas del Puerto
    
    Permisos:
    - CRUD: ADMIN, CAPITAN_PUERTO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, VIGILANTE
    - Lectura limitada: AGENTE_NAVIERO
    """
    queryset = ZonaPuerto.objects.all()
    serializer_class = ZonaPuertoSerializer
    permission_classes = [ZonaPuertoPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tipo']
    search_fields = ['nombre', 'tipo']
    ordering_fields = ['nombre', 'tipo']
    ordering = ['nombre']
