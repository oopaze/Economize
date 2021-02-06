from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import response, status

from tabelas.models import Conta
from .serializers import ContaSerializer


class ContaListView(ListAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario_fk__id=self.request.user.id).all()

        conta_id = self.request.query_params.get('id', None)
        if conta_id is not None:
            return qs.filter(id=conta_id) 

        return qs


class ContaCreateView(CreateAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        post = super().post(*args, **kwargs)
        
        if post.status_code == 201:
            instance = self.queryset.last()
            hoje = date.today()

            for parcela in range(instance.parcelas):
                mes = instance.data_compra + relativedelta(months=+parcela)
                Parcelamento.objects.create(
                    parcela = parcela,
                    conta_fk = instance,
                    mes = mes,
                    valor = instance.preco / instance.parcelas,
                ).save()

        return post


class ContaDeleteView(DestroyAPIView):
    queryset = Conta.objects.all()
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(usuario_fk__id=self.request.user.id).all()

    def delete(self, request, *args, **kwargs):
        conta = self.get_queryset().first()
        serializer = self.serializer_class(conta)
        
        super().delete(request, *args, **kwargs)
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        
