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
            if 'mes' in key:
                self.fields[key].input_formats = ['%d-%m-%Y', '%d/%m/%Y', '%m/%Y']
            self.fields[key].required = False
    
    def filter(self, qs):
        self.is_valid()
        agora = date.today().replace(day=1)
        proximo_mes = agora.replace(month=agora.month+1)

        mes_initial = self.cleaned_data.get('mes_initial', None)
        mes_final = self.cleaned_data.get('mes_final', None)
        min_value = self.cleaned_data.get('min_value', None)
        max_value = self.cleaned_data.get('max_value', None)
        search_input = self.cleaned_data.get('search_input', None)
        if mes_initial:
            qs = qs.filter(mes__gt=mes_initial)
        if mes_final:
            qs = qs.filter(mes__lt=mes_final)
        if min_value:
            qs = qs.filter(valor__gt=min_value)
        if max_value:
            qs = qs.filter(valor__lt=max_value)
        if mes_initial == mes_final and mes_initial and mes_final:
            qs = qs.filter(mes__gt=agora, mes__lt=proximo_mes)

        if search_input:
            qs1 = qs.filter(conta_fk__responsavel__icontains=search_input).values_list('id', flat=True)
            qs2 = qs.filter(conta_fk__produto__icontains=search_input).values_list('id', flat=True)
            qs3 = qs.filter(conta_fk__loja__icontains=search_input).values_list('id', flat=True)
            qs = qs.filter(id__in = [*qs1, *qs2, *qs3])

        return qs


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
        widget=forms.DateInput(
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
