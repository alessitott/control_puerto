from django.db import models
import uuid
from contenedores.models import Contenedor
from personal.models import Personal

class Inspeccion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, related_name='inspecciones')
    inspector = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, related_name='inspecciones')
    fecha = models.DateField()
    resultado = models.CharField(max_length=50)  # aprobado, rechazado, observado…
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "inspecciones"

    def __str__(self):
        return f"Inspección {self.id} - {self.contenedor.codigo_contenedor}"
