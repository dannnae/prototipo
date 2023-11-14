from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("El nombre de usuario debe ser especificado")
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener 'is_staff=True'")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener 'is_superuser=True'")

        return self._create_user(username, password, **extra_fields)

class Medico(AbstractUser):
    rut = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE, null=True)
    disponibilidad = models.ForeignKey('Disponibilidad', on_delete=models.CASCADE, null=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='medico_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='medico_user_permissions')

    def __str__(self):
        return self.nombre
    
class Paciente(AbstractUser):
    username = None
    rut = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='paciente_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='paciente_user_permissions')

    USERNAME_FIELD = 'rut'

    def __str__(self):
        return self.nombre

class Secretaria(AbstractUser):
    rut = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    # Add related_name to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='secretaria_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='secretaria_user_permissions')

class Cita(models.Model):
    fechaHora = models.DateTimeField()
    estado = models.CharField(max_length=20)
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE, null=True)
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE, null=True)
   

class Disponibilidad(models.Model):
    fecha = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    diaSemana = models.CharField(max_length=10)

class Pago(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField()
    metodoPago = models.CharField(max_length=15)
    cita = models.ForeignKey(Cita,on_delete=models.CASCADE, null=True)

class Comision(models.Model):
    monto = models.FloatField()
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE, null=True)
    fecha = models.DateField()

class Especialidad(models.Model):
    nombre = models.FloatField()

    def __str__(self):
        return self.nombre




    