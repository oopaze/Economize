from .models import Conta
from django import forms
from django.conf import settings


class ContasForm(forms.ModelForm):
    parcelas = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            if key in ['mes_de_compra', 'mes_de_pagamento']:
                self.fields[key].widget = forms.DateInput(attrs={'class': 'datepicker'})
                self.fields[key].input_formats = settings.DATE_INPUT_FORMATS

    class Meta:
        model = Conta 
        fields = '__all__'