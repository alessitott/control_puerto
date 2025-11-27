from django.urls import path, include
from rest_framework.routers import DefaultRouter
from contenedores.views import ContenedorViewSet

router = DefaultRouter()
router.register(r'contenedores', ContenedorViewSet, basename='contenedores')

urlpatterns = [
    path('', include(router.urls)),
]
