from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from personal.models import Personal
from personal.serializers import PersonalSerializer, PersonalCreateSerializer
from port_control.permissions import PersonalPermission


class PersonalViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestión de Personal del Puerto
    
    Permisos:
    - CRUD: ADMIN
    - Leer: CAPITAN_PUERTO
    - Sin acceso: Otros roles
    """
    queryset = Personal.objects.all()
    permission_classes = [PersonalPermission]
    
    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rol', 'turno', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'numero_empleado']
    ordering_fields = ['username', 'first_name', 'rol', 'date_joined']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PersonalCreateSerializer
        return PersonalSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Endpoint para obtener el perfil del usuario autenticado
        GET /api/personal/me/
        """
        serializer = PersonalSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Endpoint para actualizar el perfil propio
        PATCH /api/personal/update_profile/
        """
        user = request.user
        # Solo permitir actualizar ciertos campos
        allowed_fields = ['first_name', 'last_name', 'email', 'telefono']
        data = {k: v for k, v in request.data.items() if k in allowed_fields}
        
        serializer = PersonalSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
