from rest_framework import serializers
from autorizaciones.models import Autorizacion

class AutorizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autorizacion
        fields = '__all__'
