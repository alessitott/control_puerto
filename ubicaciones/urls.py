"""
URLs para el sistema de ubicación de buques.
"""
from django.urls import path
from ubicaciones import views

app_name = 'ubicaciones'

urlpatterns = [
    # Prueba de conexión
    path('test/', views.test_mongo_connection, name='test-connection'),
    
    # Registro de ubicaciones
    path('registrar/', views.registrar_ubicacion, name='registrar-ubicacion'),
    
    # Consultas
    path('actuales/', views.obtener_ubicaciones_actuales, name='ubicaciones-actuales'),
    path('barco/<str:barco_id>/', views.obtener_ultima_ubicacion, name='ultima-ubicacion'),
    path('barco/<str:barco_id>/historial/', views.obtener_historial, name='historial-ubicaciones'),
    path('cercanos/', views.buscar_buques_cercanos, name='buques-cercanos'),
    
    # Simulación
    path('simulacion/iniciar/', views.iniciar_simulacion, name='iniciar-simulacion'),
    path('simulacion/detener/', views.detener_simulacion, name='detener-simulacion'),
    path('simulacion/estado/', views.estado_simulacion, name='estado-simulacion'),
]

