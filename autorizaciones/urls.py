from django.urls import path, include
from rest_framework.routers import DefaultRouter
from autorizaciones.views import AutorizacionViewSet

router = DefaultRouter()
router.register(r'autorizaciones', AutorizacionViewSet, basename='autorizaciones')

urlpatterns = [
    path('', include(router.urls)),
]
