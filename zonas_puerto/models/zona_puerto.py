from django.db import models
import uuid

class ZonaPuerto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = "zonas_puerto"

    def __str__(self):
        return self.nombre
