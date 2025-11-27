from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Autenticación JWT
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # APIs de entidades
    path('api/', include('barcos.urls')),
    path('api/', include('tripulacion.urls')),
    path('api/', include('contenedores.urls')),
    path('api/', include('zonas_puerto.urls')),
    path('api/', include('personal.urls')),
    path('api/', include('movimientos.urls')),
    path('api/', include('inspecciones.urls')),
    path('api/', include('autorizaciones.urls')),
]



