from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from contas.models import Conta
from contas.forms import ContasForm
from .mixins import GetMultipleItensMixin


class ContaCreateView(CreateView):
    template_name='base/create_update.html'
    model = Conta
    form_class = ContasForm
    success_url = reverse_lazy('contas-list')

    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        if self.object:
            self.object.generate_parcelas()
        return response        


class ContaDeleteView(DeleteView):
    model = Conta
    success_url = reverse_lazy('contas-list')

    def get(self, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return redirect(self.success_url)
        


class ContaListView(ListView, GetMultipleItensMixin):
    template_name='base/listview.html'
    model= Conta

    def get_columns(self):
        return (
            'produto', 
            'valor', 
            'local', 
            'responsavel', 
            'mes de compra', 
            'mes de pagamento', 
            'parcelas',
            'ações'
        )

    def get_item(self, item):
        url = reverse_lazy('conta-delete', args=[item.pk])
        btn_delete = f"<a class='btn btn-danger' href='{ url }'> Deletar Conta </a>"

        return (
            item.produto,
            item.valor,
            item.local,
            item.responsavel,
            item.mes_de_compra,
            item.mes_de_pagamento,
            item.parcelas,
            btn_delete
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['columns'] = self.get_columns()
        ctx['itens'] = self.get_itens()
        return ctx