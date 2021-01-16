from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import response, status

from tabelas.models import Conta, Parcelamento
from .serializers import ContaSerializer, ParcelasSerializer


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


class ParcelasListView(ListAPIView):
    serializer_class = ParcelasSerializer
    permission_classes = [IsAuthenticated]
    paginate_by = 20


    def get_queryset(self, *args, **kwargs):
        qs = Parcelamento.objects.filter(conta_fk__usuario_fk__id=self.request.user.id).all()

        mes = self.request.query_params.get('mes', None)
        pago = self.request.query_params.get('pago', None)
        responsavel = self.request.query_params.get('responsavel', None)

        if mes is not None:
            mes = datetime.strptime(mes, "%d/%m/%Y").date()
            qs = qs.filter(mes=mes)

        if pago is not None:
            qs = qs.filter(pago=pago)
        
        if responsavel is not None:
            qs = qs.filter(conta_fk__responsavel__icontains=responsavel)

        return qs 

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.format_serializer(page)
            return self.get_paginated_response(data)

        data = self.format_serializer(queryset)
        return response.Response(data)

    def format_serializer(self, qs):
        dados = {
            'contas': [],
            'total': 0,
            'total_pago': 0,
            'a_pagar': 0
        }
        for item in qs.all():
            parcela = self.get_serializer(item).data
            data = {
                'info':{
                    'produto': item.conta_fk.produto,
                    'loja': item.conta_fk.loja,
                    'preco_total': item.conta_fk.preco,
                }
            }
            data.update(parcela)
            data.pop('conta_fk', None)
            dados['contas'].append(data)
            dados['total'] += item.valor
            dados['total_pago'] += item.valor if item.pago else 0
            dados['a_pagar'] += item.valor if not item.pago else 0

        return dados


class ParcelaUpdateView(UpdateAPIView):
    queryset = Parcelamento.objects.all()
    serializer_class = ParcelasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(conta_fk__usuario_fk__id=self.request.user.id).all()

    def get_serializer(self, *args, **kwargs):
        instance = args[0]
        kwargs['partial'] = True
        kwargs['data'] = {'pago': not instance.pago, 'pago_data': date.today()}
        return super().get_serializer(*args, **kwargs)

    def put(self, *args, **kwargs):
        try:
            return super().put(*args, **kwargs)
        except KeyError:
            return response.Response({
                'error': 'Somente o atributo "pago" pode ser editado.',
            }, status.HTTP_406_NOT_ACCEPTABLE)


class PayParcelaUpdateView(UpdateAPIView):
    serializer_class = ParcelasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Parcelamento.objects.filter(
            conta_fk__usuario_fk = self.request.user
        )
    
    def put(self, *args, **kwargs):
        print(args)
        print(kwargs)
        return super().put(*args, **kwargs)
        
