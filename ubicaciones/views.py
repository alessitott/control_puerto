"""
Vistas para el sistema de ubicación en tiempo real de buques.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta

from ubicaciones.models import UbicacionBuque
from ubicaciones.serializers import UbicacionBuqueSerializer, BusquedaCercanosSerializer
from ubicaciones.services import simulador
from port_control.mongodb import test_connection
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_mongo_connection(request):
    """
    Endpoint para probar la conexión a MongoDB.
    """
    try:
        if test_connection():
            return Response({
                'success': True,
                'message': 'Conexión a MongoDB exitosa'
            })
        else:
            return Response({
                'success': False,
                'message': 'Error al conectar a MongoDB'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_ubicacion(request):
    """
    Registra una nueva ubicación de un buque.
    POST /api/ubicaciones/registrar/
    """
    try:
        serializer = UbicacionBuqueSerializer(data=request.data)
        if serializer.is_valid():
            ubicacion = UbicacionBuque(
                barco_id=str(serializer.validated_data['barco_id']),
                latitud=serializer.validated_data['latitud'],
                longitud=serializer.validated_data['longitud'],
                velocidad=serializer.validated_data.get('velocidad', 0.0),
                rumbo=serializer.validated_data.get('rumbo', 0.0),
                timestamp=serializer.validated_data.get('timestamp'),
                estado=serializer.validated_data.get('estado', 'en_transito'),
                metadata=serializer.validated_data.get('metadata', {})
            )
            
            ubicacion_id = ubicacion.save()
            
            return Response({
                'success': True,
                'message': 'Ubicación registrada exitosamente',
                'id': ubicacion_id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error al registrar ubicación: {e}")
        return Response({
            'success': False,
            'message': f'Error al registrar ubicación: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_ultima_ubicacion(request, barco_id):
    """
    Obtiene la última ubicación registrada de un barco.
    GET /api/ubicaciones/barco/{barco_id}/
    """
    try:
        ubicacion = UbicacionBuque.get_ultima_ubicacion(barco_id)
        
        if ubicacion:
            serializer = UbicacionBuqueSerializer(ubicacion)
            return Response({
                'success': True,
                'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'No se encontró ubicación para este barco'
            }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        logger.error(f"Error al obtener ubicación: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_ubicaciones_actuales(request):
    """
    Obtiene la última ubicación de todos los barcos.
    GET /api/ubicaciones/actuales/
    """
    try:
        ubicaciones = UbicacionBuque.get_todas_ubicaciones_actuales()
        
        serializer = UbicacionBuqueSerializer(ubicaciones, many=True)
        
        return Response({
            'success': True,
            'count': len(ubicaciones),
            'data': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Error al obtener ubicaciones actuales: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_historial(request, barco_id):
    """
    Obtiene el historial de ubicaciones de un barco en un rango de tiempo.
    GET /api/ubicaciones/barco/{barco_id}/historial/?inicio=2024-01-01T00:00:00&fin=2024-01-02T00:00:00
    """
    try:
        inicio_str = request.query_params.get('inicio')
        fin_str = request.query_params.get('fin')
        
        if not inicio_str or not fin_str:
            # Por defecto, últimas 24 horas
            fin = timezone.now()
            inicio = fin - timedelta(hours=24)
        else:
            inicio = datetime.fromisoformat(inicio_str.replace('Z', '+00:00'))
            fin = datetime.fromisoformat(fin_str.replace('Z', '+00:00'))
        
        ubicaciones = UbicacionBuque.get_ubicaciones_por_rango_tiempo(
            barco_id, inicio, fin
        )
        
        serializer = UbicacionBuqueSerializer(ubicaciones, many=True)
        
        return Response({
            'success': True,
            'count': len(ubicaciones),
            'inicio': inicio.isoformat(),
            'fin': fin.isoformat(),
            'data': serializer.data
        })
        
    except Exception as e:
        logger.error(f"Error al obtener historial: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buscar_buques_cercanos(request):
    """
    Busca buques cercanos a un punto geográfico.
    POST /api/ubicaciones/cercanos/
    Body: {"latitud": 8.9824, "longitud": -79.5199, "radio_km": 10.0}
    """
    try:
        serializer = BusquedaCercanosSerializer(data=request.data)
        if serializer.is_valid():
            latitud = serializer.validated_data['latitud']
            longitud = serializer.validated_data['longitud']
            radio_km = serializer.validated_data.get('radio_km', 10.0)
            
            ubicaciones = UbicacionBuque.get_buques_cercanos(
                latitud, longitud, radio_km
            )
            
            serializer_ubicaciones = UbicacionBuqueSerializer(ubicaciones, many=True)
            
            return Response({
                'success': True,
                'count': len(ubicaciones),
                'punto_central': {
                    'latitud': latitud,
                    'longitud': longitud
                },
                'radio_km': radio_km,
                'data': serializer_ubicaciones.data
            })
        else:
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error al buscar buques cercanos: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def iniciar_simulacion(request):
    """
    Inicia la simulación de ubicaciones en tiempo real.
    POST /api/ubicaciones/simulacion/iniciar/
    Body opcional: {"intervalo_segundos": 30}
    """
    try:
        intervalo = request.data.get('intervalo_segundos', 30)
        
        if intervalo < 5:
            return Response({
                'success': False,
                'message': 'El intervalo mínimo es 5 segundos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        simulador.iniciar(intervalo)
        
        return Response({
            'success': True,
            'message': f'Simulación iniciada con intervalo de {intervalo} segundos'
        })
        
    except Exception as e:
        logger.error(f"Error al iniciar simulación: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detener_simulacion(request):
    """
    Detiene la simulación de ubicaciones.
    POST /api/ubicaciones/simulacion/detener/
    """
    try:
        simulador.detener()
        
        return Response({
            'success': True,
            'message': 'Simulación detenida'
        })
        
    except Exception as e:
        logger.error(f"Error al detener simulación: {e}")
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_simulacion(request):
    """
    Obtiene el estado de la simulación.
    GET /api/ubicaciones/simulacion/estado/
    """
    return Response({
        'success': True,
        'activa': simulador.activo,
        'intervalo_segundos': simulador.intervalo_segundos if simulador.activo else None
    })

