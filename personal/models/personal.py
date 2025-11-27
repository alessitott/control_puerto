from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Personal(AbstractUser):
    """
    Modelo de Personal del Puerto - Extiende AbstractUser para autenticación
    """
    
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador del Sistema'
        CAPITAN_PUERTO = 'CAPITAN_PUERTO', 'Capitán de Puerto'
        OPERADOR_TERMINAL = 'OPERADOR_TERMINAL', 'Operador de Terminal'
        INSPECTOR = 'INSPECTOR', 'Inspector de Seguridad/Aduanas'
        AGENTE_NAVIERO = 'AGENTE_NAVIERO', 'Agente Naviero'
        VIGILANTE = 'VIGILANTE', 'Vigilante/Seguridad'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Campos adicionales del personal del puerto
    rol = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.VIGILANTE,
        verbose_name='Rol en el Puerto'
    )
    turno = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Turno de Trabajo'
    )
    numero_empleado = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Número de Empleado'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    class Meta:
        db_table = "personal"
        verbose_name = "Personal"
        verbose_name_plural = "Personal"
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} - {self.get_rol_display()}"
    
    # Métodos de verificación de rol
    @property
    def is_admin(self):
        return self.rol == self.Roles.ADMIN or self.is_superuser
    
    @property
    def is_capitan_puerto(self):
        return self.rol == self.Roles.CAPITAN_PUERTO
    
    @property
    def is_operador_terminal(self):
        return self.rol == self.Roles.OPERADOR_TERMINAL
    
    @property
    def is_inspector(self):
        return self.rol == self.Roles.INSPECTOR
    
    @property
    def is_agente_naviero(self):
        return self.rol == self.Roles.AGENTE_NAVIERO
    
    @property
    def is_vigilante(self):
        return self.rol == self.Roles.VIGILANTE
