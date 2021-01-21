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


class FilterParcelasForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for key in self.fields.keys():
            self.fields[key].required = False
    
    def filter(self, qs, params):
        ...


    mes_initial = forms.DateField(
        label="Data inicial",
        widget=forms.TextInput(
            attrs = {
                'class': 'date-picker',
                'placeholder': 'Data Inicial'
            }
        )
    )
    mes_final = forms.DateField(
        label = 'Data Final',
        widget=forms.TextInput(
            attrs = {
                'class': 'date-picker',
                'placeholder': 'Data Final'
            }
        )
    )
    min_value = forms.DecimalField(
        label='Preço Mínimo da parcela',
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Preço Mínimo da parcela'
            }
        )
    )
    max_value = forms.DecimalField(
        label='Preço Máximo da parcela',
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Preço Máximo da parcela'
            }
        )
    )
    search_input = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Procure por valor, loja ou produto'
            }
        )
    )
