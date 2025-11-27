"""
Manejador de excepciones personalizado para el Control de Puerto Marítimo
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    AuthenticationFailed,
    PermissionDenied,
    NotFound,
)


def custom_exception_handler(exc, context):
    """
    Manejador de excepciones personalizado que formatea las respuestas de error
    de manera consistente.
    
    Formato de respuesta:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Mensaje legible para el usuario",
            "details": {...}  # Opcional, detalles adicionales
        }
    }
    """
    
    # Primero obtener la respuesta estándar de DRF
    response = exception_handler(exc, context)
    
    # Si DRF no manejó la excepción, manejarla aquí
    if response is None:
        if isinstance(exc, DjangoValidationError):
            return Response({
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Error de validación",
                    "details": exc.messages if hasattr(exc, 'messages') else str(exc)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Error interno del servidor
        return Response({
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Ha ocurrido un error interno en el servidor",
                "details": str(exc) if str(exc) else None
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Formatear respuestas de DRF
    error_response = {
        "success": False,
        "error": {
            "code": get_error_code(exc),
            "message": get_error_message(exc),
            "details": response.data if response.data else None
        }
    }
    
    response.data = error_response
    return response


def get_error_code(exc):
    """Obtiene un código de error legible basado en el tipo de excepción"""
    
    error_codes = {
        ValidationError: "VALIDATION_ERROR",
        NotAuthenticated: "NOT_AUTHENTICATED",
        AuthenticationFailed: "AUTHENTICATION_FAILED",
        PermissionDenied: "PERMISSION_DENIED",
        NotFound: "NOT_FOUND",
        Http404: "NOT_FOUND",
    }
    
    for exc_class, code in error_codes.items():
        if isinstance(exc, exc_class):
            return code
    
    return "UNKNOWN_ERROR"


def get_error_message(exc):
    """Obtiene un mensaje de error legible para el usuario"""
    
    error_messages = {
        ValidationError: "Los datos proporcionados no son válidos",
        NotAuthenticated: "Debes iniciar sesión para acceder a este recurso",
        AuthenticationFailed: "Las credenciales proporcionadas son incorrectas",
        PermissionDenied: "No tienes permiso para realizar esta acción",
        NotFound: "El recurso solicitado no fue encontrado",
        Http404: "El recurso solicitado no fue encontrado",
    }
    
    for exc_class, message in error_messages.items():
        if isinstance(exc, exc_class):
            return message
    
    # Si tiene un mensaje personalizado, usarlo
    if hasattr(exc, 'detail'):
        return str(exc.detail)
    
    return "Ha ocurrido un error inesperado"

