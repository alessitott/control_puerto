from django.db import models
import uuid
from contenedores.models import Contenedor
from zonas_puerto.models import ZonaPuerto
from personal.models import Personal

class Movimiento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=50)  # ingreso, salida, traslado…
    zona_origen = models.ForeignKey(ZonaPuerto, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_origen')
    zona_destino = models.ForeignKey(ZonaPuerto, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_destino')
    fecha_hora = models.DateTimeField()
    operador = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='movimientos')

    class Meta:
        db_table = "movimientos"

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.contenedor.codigo_contenedor}"
