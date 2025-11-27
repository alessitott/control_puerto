from rest_framework import serializers
from contenedores.models import Contenedor

class ContenedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenedor
        fields = '__all__'
