from django.db import models
import uuid
from barcos.models import Barco

class Contenedor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barco = models.ForeignKey(Barco, on_delete=models.CASCADE, related_name='contenedores')
    codigo_contenedor = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50)
    peso = models.FloatField()
    estado = models.CharField(max_length=50)

    class Meta:
        db_table = "contenedores"

    def __str__(self):
        return self.codigo_contenedor
