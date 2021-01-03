from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/images')


class Conta(models.Model):
    usuario_fk = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    produto = models.CharField(max_length=255, null=True, blank=True)
    loja = models.CharField(max_length=255, null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=15)
    parcelas = models.PositiveIntegerField()


class Parcelamento(models.Model):
    conta_fk = models.ForeignKey('Conta', on_delete=models.CASCADE)
    mes = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    pago = models.BooleanField(default=False)
    
