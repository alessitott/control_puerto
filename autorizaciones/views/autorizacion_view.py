from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from autorizaciones.models import Autorizacion
from autorizaciones.serializers import AutorizacionSerializer
from port_control.permissions import AutorizacionPermission


class AutorizacionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Autorizaciones
    
    Permisos:
    - CRUD: ADMIN, CAPITAN_PUERTO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    queryset = Autorizacion.objects.all()
    serializer_class = AutorizacionSerializer
    permission_classes = [AutorizacionPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['barco', 'autorizado_por', 'tipo_autorizacion', 'estado', 'fecha']
    search_fields = ['tipo_autorizacion', 'estado', 'barco__nombre']
    ordering_fields = ['fecha', 'estado', 'tipo_autorizacion']
    ordering = ['-fecha']
