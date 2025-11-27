from rest_framework import serializers
from inspecciones.models import Inspeccion

class InspeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspeccion
        fields = '__all__'
