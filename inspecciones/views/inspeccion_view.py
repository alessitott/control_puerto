from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from inspecciones.models import Inspeccion
from inspecciones.serializers import InspeccionSerializer
from port_control.permissions import InspeccionPermission


class InspeccionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Inspecciones
    
    Permisos:
    - CRUD: ADMIN, INSPECTOR
    - Leer: CAPITAN_PUERTO, OPERADOR_TERMINAL, VIGILANTE
    - Sin acceso: AGENTE_NAVIERO
    """
    queryset = Inspeccion.objects.all()
    serializer_class = InspeccionSerializer
    permission_classes = [InspeccionPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contenedor', 'inspector', 'resultado', 'fecha']
    search_fields = ['resultado', 'observaciones', 'contenedor__codigo_contenedor']
    ordering_fields = ['fecha', 'resultado']
    ordering = ['-fecha']
