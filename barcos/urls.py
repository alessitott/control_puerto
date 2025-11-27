from django.urls import path, include
from rest_framework.routers import DefaultRouter
from barcos.views import BarcoViewSet

router = DefaultRouter()
router.register(r'barcos', BarcoViewSet, basename='barcos')

urlpatterns = [
    path('', include(router.urls)),
]
