from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework import response, status
from django.shortcuts import render

from tabelas.models import Contas
from .serializers import ContaSerializer


class ContaListView(ListAPIView):
    queryset = Contas.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAdminUser]


class ContaCreateView(CreateAPIView):
    queryset = Contas.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAdminUser]


class ContaUpdateView(UpdateAPIView):
    queryset = Contas.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAdminUser]


class ContaDeleteView(DestroyAPIView):
    queryset = Contas.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        conta = self.get_queryset().first()
        serializer = self.serializer_class(conta)
        
        super().delete(request, *args, **kwargs)

        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)