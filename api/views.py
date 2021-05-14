from dateutil.relativedelta import relativedelta
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.utils.timezone import now
from django.db.models import Q

from .serializers import ContaSerializer, ParcelaSerializer
from contas.models import Conta, Parcela


class ContaViewSet(ModelViewSet):
    serializer_class = ContaSerializer
    queryset = Conta.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.generate_parcelas()
        return instance


class ParcelaViewSet(ReadOnlyModelViewSet, UpdateModelMixin):
    serializer_class = ParcelaSerializer
    queryset = Parcela.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        este_mes = now().replace(day=1)
        proximo_mes = este_mes + relativedelta(months=+1)

        return qs.filter(Q(data__lt=proximo_mes, data__gte=este_mes) | Q(data__lt=proximo_mes, pago=False))

        