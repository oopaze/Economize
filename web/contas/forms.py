from datetime import date

from django import forms
from django.contrib.postgres.forms import SimpleArrayField

from tabelas.models import Parcelamento


class PayManyParcelaForm(forms.Form):
    parcela_ids = SimpleArrayField(
        forms.IntegerField()
    )

    def save(self):
        pks = self.data['parcela_ids']
        parcelas = Parcelamento.objects.filter(id__in = pks)
        for parcela in parcelas:
            parcela.pago=True
            parcela.data_pago=date.today()
            parcela.save()


class FilterParcelasForm(forms.ModelForm):
    class Meta:
        model = Parcelamento
        fields = '__all__'
