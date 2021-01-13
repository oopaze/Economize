from rest_framework import serializers
from tabelas.models import Conta, Parcelamento


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = '__all__'


class ParcelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelamento
        fields = '__all__'