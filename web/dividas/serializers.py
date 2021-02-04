from rest_framework import serializers
from tabelas.models import Conta, Parcelamento


class ParcelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelamento
        fields = '__all__'