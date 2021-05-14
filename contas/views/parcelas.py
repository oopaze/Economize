from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from contas.models import Parcela
from .mixins import GetMultipleItensMixin


class ParcelaListView(ListView, GetMultipleItensMixin):
    template_name='base/listview.html'
    model = Parcela

    def get_queryset(self):
        qs = super().get_queryset()
        conta_id = self.request.GET.get('conta_id', None)
        if conta_id:
            qs = qs.filter(conta_fk_id = conta_id)
        return qs

    def get_columns(self):
        return ('Produto', "Valor", "Loja", "Data de Pagamento", "Data de Compra")

    def get_item(self, item):
        return (
            item.conta_fk.produto,
            item.valor,
            item.conta_fk.local,
            item.data,
            item.conta_fk.mes_de_compra
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['columns'] = self.get_columns()
        ctx['itens'] = self.get_itens()
        return ctx