from django.db import models
import uuid
from barcos.models import Barco

class Tripulante(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barco = models.ForeignKey(Barco, on_delete=models.CASCADE, related_name='tripulacion')
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50)

    class Meta:
        db_table = "tripulacion"

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
