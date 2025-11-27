from django.db import models
import uuid

class Barco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    bandera = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    empresa_operadora = models.CharField(max_length=100)
    fecha_llegada = models.DateField(null=True, blank=True)
    fecha_salida = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "barcos"

    def __str__(self):
        return self.nombre
