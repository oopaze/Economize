from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Usuario(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/images')
    ganho_mensal = models.DecimalField(decimal_places=2, max_digits=12)


class Conta(models.Model):
    usuario_fk = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    responsavel = models.CharField(max_length=255)
    produto = models.CharField(max_length=255, null=True, blank=True)
    loja = models.CharField(max_length=255, null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=15)
    parcelas = models.PositiveIntegerField()
    data_compra = models.DateField()

    def count_parcelas(self):
        parcelas = self.parcelamento_set.all()
        total = parcelas.count()
        pago = parcelas.filter(pago=True).count()
        return f"{pago}/{total}"
    
    def check_pago(self):
        pago = self.parcelamento_set.filter(pago=False).count()
        if pago > 0:
            return False
        return True
    
    def gasto():
        value = sum(Conta.objects.all().values_list('preco', flat=True))
        value = f"{value:,.2f}".replace(',', '|')
        value = value.replace('.', ',')
        value = value.replace('|', '.')
        return value


class Parcelamento(models.Model):
    parcela = models.IntegerField()
    conta_fk = models.ForeignKey('Conta', on_delete=models.CASCADE)
    mes = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    pago = models.BooleanField(default=False)
    data_pago = models.DateField(null=True, blank=True)
    
