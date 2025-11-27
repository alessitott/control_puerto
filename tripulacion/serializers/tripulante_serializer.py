from rest_framework import serializers
from tripulacion.models import Tripulante

class TripulanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tripulante
        fields = '__all__'
