from django.urls import path, include
from rest_framework.routers import DefaultRouter
from zonas_puerto.views import ZonaPuertoViewSet

router = DefaultRouter()
router.register(r'zonas-puerto', ZonaPuertoViewSet, basename='zonas-puerto')

urlpatterns = [
    path('', include(router.urls)),
]
