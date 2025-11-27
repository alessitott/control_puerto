from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from tripulacion.models import Tripulante
from tripulacion.serializers import TripulanteSerializer
from port_control.permissions import TripulacionPermission


class TripulanteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Tripulación
    
    Permisos:
    - CRUD: ADMIN, AGENTE_NAVIERO
    - Leer: CAPITAN_PUERTO, INSPECTOR, VIGILANTE
    - Sin acceso: OPERADOR_TERMINAL
    """
    queryset = Tripulante.objects.all()
    serializer_class = TripulanteSerializer
    permission_classes = [TripulacionPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['barco', 'rol', 'nacionalidad']
    search_fields = ['nombre', 'rol', 'nacionalidad', 'identificacion']
    ordering_fields = ['nombre', 'rol']
    ordering = ['nombre']
