from django.db import models
import uuid
from barcos.models import Barco
from personal.models import Personal

class Autorizacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barco = models.ForeignKey(Barco, on_delete=models.CASCADE, related_name='autorizaciones')
    autorizado_por = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='autorizaciones')
    fecha = models.DateField()
    tipo_autorizacion = models.CharField(max_length=100)  # entrada, salida, carga, descarga, etc.
    estado = models.CharField(max_length=50)  # aprobada, rechazada, pendiente

    class Meta:
        db_table = "autorizaciones"

    def __str__(self):
        return f"{self.tipo_autorizacion} - {self.barco.nombre}"
