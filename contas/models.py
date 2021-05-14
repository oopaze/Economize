from django.db import models
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


class Conta(models.Model):
    produto = models.CharField(max_length=255)
    valor = models.FloatField()
    local = models.CharField(max_length=255, null=True, blank=True)
    responsavel = models.CharField(max_length=255, default="Eu mesmo.")
    pago = models.BooleanField(default=False)
    mes_de_compra = models.DateField(default=now)
    mes_de_pagamento = models.DateField()
    parcelas = models.IntegerField(default=1)

    def generate_parcelas(self, *args, **kwargs):
        for i in range(0, self.parcelas):
            valor_parcela = round(self.valor / self.parcelas, 2)
            parcela = Parcela.objects.create(
                conta_fk = self,
                valor = valor_parcela, 
                data = self.mes_de_pagamento + relativedelta(months=+i)
            )
            parcela.save()

    def update_pago(self):
        parcelas = self.parcelas_set.filter(pago = False)
        if not parcelas.exists():
            self.pago = True
            self.save()


class Parcela(models.Model):
    valor = models.FloatField()
    conta_fk = models.ForeignKey('Conta', on_delete=models.CASCADE)
    data = models.DateField()
    pago = models.BooleanField(default=False)