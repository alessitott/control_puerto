from django.urls import path, include
from rest_framework.routers import DefaultRouter
from personal.views import PersonalViewSet

router = DefaultRouter()
router.register(r'personal', PersonalViewSet, basename='personal')

urlpatterns = [
    path('', include(router.urls)),
]
