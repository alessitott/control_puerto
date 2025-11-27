from rest_framework import serializers
from zonas_puerto.models import ZonaPuerto

class ZonaPuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZonaPuerto
        fields = '__all__'
