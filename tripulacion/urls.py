from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tripulacion.views import TripulanteViewSet

router = DefaultRouter()
router.register(r'tripulacion', TripulanteViewSet, basename='tripulacion')

urlpatterns = [
    path('', include(router.urls)),
]
