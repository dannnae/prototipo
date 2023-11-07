from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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


class Usuario(AbstractUser):
    apellido = models.CharField(max_length=20)
    objects = CustomUserManager()
    comuna = models.ForeignKey('Comuna',on_delete=models.CASCADE, null=True)

class Medico(models.Model):
    rut = models.CharField(max_length=10)
    nombre = models.CharField()
    especialidad = models.CharField()
    #disponibilidad: Disponibilidad

class Paciente(models.Model):
    rut = models.CharField(max_length=10)
    nombre = models.CharField()
    email = models.CharField()
    telefono = models.IntegerField(max_length=13)

class Cita(models.Model):
    fechaHora = models.DateTimeField()
    estado = models.CharField()
    #medico: Medico
    #paciente : Paciente

class Disponibilidad(models.Model):
    fecha = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
    diaSemana = models.CharField()

class Pago(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField()
    metodoPago = models.CharField()
    #cita : Cita

class Comision(models.Model):
    monto = models.FloatField()
    #medico : Medico
    fecha = models.DateField()



    