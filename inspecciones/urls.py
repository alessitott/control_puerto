from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inspecciones.views import InspeccionViewSet

router = DefaultRouter()
router.register(r'inspecciones', InspeccionViewSet, basename='inspecciones')

urlpatterns = [
    path('', include(router.urls)),
]
