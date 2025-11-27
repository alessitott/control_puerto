from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contenedores.models import Contenedor
from contenedores.serializers import ContenedorSerializer
from port_control.permissions import ContenedorPermission


class ContenedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Contenedores
    
    Permisos:
    - CRUD: ADMIN, CAPITAN_PUERTO, OPERADOR_TERMINAL
    - Leer: INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    queryset = Contenedor.objects.all()
    serializer_class = ContenedorSerializer
    permission_classes = [ContenedorPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['barco', 'tipo', 'estado']
    search_fields = ['codigo_contenedor', 'tipo', 'estado']
    ordering_fields = ['codigo_contenedor', 'peso', 'tipo']
    ordering = ['codigo_contenedor']
