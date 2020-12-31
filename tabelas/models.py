from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/images')


class Contas(models.Model):
    usuario_fk = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    produto = models.CharField(max_length=255, null=True, blank=True)
    loja = models.CharField(max_length=255, null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=15)