from rest_framework import serializers
from tabelas.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].default = True
        self.fields['is_active'].default = True
        
    class Meta:
        model = Usuario
        fields = [
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active'
        ]


class UsuarioReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active'
        ]

