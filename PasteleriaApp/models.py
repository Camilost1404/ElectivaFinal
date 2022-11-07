from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=60)
    telefono = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Pedido(models.Model):
    codigo_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    estado = models.CharField(max_length=45)
    tipo_entrega = models.CharField(max_length=45)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class Sabor(models.Model):
    nombre_sabor = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Relleno(models.Model):
    nombre_relleno = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Cobertura(models.Model):
    nombre_cobertura = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Producto(models.Model):
    sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE)
    relleno = models.ForeignKey(Relleno, on_delete=models.CASCADE)
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    tamaño = models.IntegerField()
    aclaracion = models.CharField(max_length=45)


class detalle_pedido(models.Model):
    codigo_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    codigo_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
