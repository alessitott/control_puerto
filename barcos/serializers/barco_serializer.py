from rest_framework import serializers
from barcos.models import Barco

class BarcoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barco
        fields = '__all__'
