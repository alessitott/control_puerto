"""
Permisos personalizados para el Control de Puerto Marítimo

Matriz de permisos:
- ADMIN: CRUD en todo
- CAPITAN_PUERTO: CRUD en barcos, contenedores, zonas, movimientos, autorizaciones; Leer personal, tripulación, inspecciones
- OPERADOR_TERMINAL: CRUD en contenedores, movimientos; Leer barcos, zonas, inspecciones, autorizaciones
- INSPECTOR: CRUD en inspecciones; Leer barcos, tripulación, contenedores, zonas, movimientos, autorizaciones
- AGENTE_NAVIERO: CRUD en barcos, tripulación; Leer contenedores, movimientos, autorizaciones
- VIGILANTE: Solo lectura en todo
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Solo administradores tienen acceso"""
    message = "Solo los administradores pueden realizar esta acción."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Administradores: CRUD, Otros: Solo lectura"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin


# ============ PERMISOS POR ENTIDAD ============

class BarcoPermission(BasePermission):
    """
    Barcos:
    - CRUD: ADMIN, CAPITAN_PUERTO, AGENTE_NAVIERO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, VIGILANTE
    """
    message = "No tienes permiso para esta acción sobre barcos."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # Lectura permitida para todos los roles autenticados
        if request.method in SAFE_METHODS:
            return True
        
        # CRUD para roles específicos
        return user.is_admin or user.is_capitan_puerto or user.is_agente_naviero


class TripulacionPermission(BasePermission):
    """
    Tripulación:
    - CRUD: ADMIN, AGENTE_NAVIERO
    - Leer: CAPITAN_PUERTO, INSPECTOR, VIGILANTE
    - Sin acceso: OPERADOR_TERMINAL
    """
    message = "No tienes permiso para esta acción sobre tripulación."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # Sin acceso para operador terminal
        if user.is_operador_terminal:
            return False
        
        # Lectura para roles permitidos
        if request.method in SAFE_METHODS:
            return True
        
        # CRUD para roles específicos
        return user.is_admin or user.is_agente_naviero


class ContenedorPermission(BasePermission):
    """
    Contenedores:
    - CRUD: ADMIN, CAPITAN_PUERTO, OPERADOR_TERMINAL
    - Leer: INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    message = "No tienes permiso para esta acción sobre contenedores."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.is_admin or user.is_capitan_puerto or user.is_operador_terminal


class ZonaPuertoPermission(BasePermission):
    """
    Zonas del Puerto:
    - CRUD: ADMIN, CAPITAN_PUERTO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, VIGILANTE
    - Sin acceso: AGENTE_NAVIERO
    """
    message = "No tienes permiso para esta acción sobre zonas del puerto."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # Sin acceso para agente naviero
        if user.is_agente_naviero:
            return request.method in SAFE_METHODS  # Solo lectura limitada
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.is_admin or user.is_capitan_puerto


class PersonalPermission(BasePermission):
    """
    Personal:
    - CRUD: ADMIN
    - Leer: CAPITAN_PUERTO
    - Sin acceso: Otros roles
    """
    message = "No tienes permiso para esta acción sobre personal."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # CRUD solo para admin
        if user.is_admin:
            return True
        
        # Lectura solo para capitán de puerto
        if user.is_capitan_puerto and request.method in SAFE_METHODS:
            return True
        
        return False


class MovimientoPermission(BasePermission):
    """
    Movimientos:
    - CRUD: ADMIN, CAPITAN_PUERTO, OPERADOR_TERMINAL
    - Leer: INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    message = "No tienes permiso para esta acción sobre movimientos."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.is_admin or user.is_capitan_puerto or user.is_operador_terminal


class InspeccionPermission(BasePermission):
    """
    Inspecciones:
    - CRUD: ADMIN, INSPECTOR
    - Leer: CAPITAN_PUERTO, OPERADOR_TERMINAL, VIGILANTE
    - Sin acceso: AGENTE_NAVIERO
    """
    message = "No tienes permiso para esta acción sobre inspecciones."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        # Sin acceso para agente naviero
        if user.is_agente_naviero:
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.is_admin or user.is_inspector


class AutorizacionPermission(BasePermission):
    """
    Autorizaciones:
    - CRUD: ADMIN, CAPITAN_PUERTO
    - Leer: OPERADOR_TERMINAL, INSPECTOR, AGENTE_NAVIERO, VIGILANTE
    """
    message = "No tienes permiso para esta acción sobre autorizaciones."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        
        if request.method in SAFE_METHODS:
            return True
        
        return user.is_admin or user.is_capitan_puerto

