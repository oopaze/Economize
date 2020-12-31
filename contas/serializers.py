from rest_framework import serializers
from tabelas.models import Contas


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contas
        fields = '__all__'