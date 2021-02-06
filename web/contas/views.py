from django.views.generic import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tabelas.models import Conta


class ContaListView(LoginRequiredMixin, ListView):
    template_name = 'contas/table_list.html'
    model = Conta
    context_object_name = 'items'
    paginate_by = 15
    allow_empty=True

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(usuario_fk = self.request.user)

    def get_columns(self):
        return ('', 'Responsável', 'Produto', 'Loja', 'Preço', 'Parcelas', 'Data Compra')

    def get_context_data(self):
        context = super().get_context_data()
        context['columns'] = self.get_columns()
        context['total_gasto'] = self.model.gasto()
        return context