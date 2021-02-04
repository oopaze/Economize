from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.views.generic import ListView, FormView, View, UpdateView   
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tabelas.models import Parcelamento
from .forms import PayManyParcelaForm, FilterParcelasForm


class HomeListView(LoginRequiredMixin, ListView, FormView):
    template_name = 'index.html'
    model = Parcelamento
    form_class = FilterParcelasForm
    context_object_name = 'contas'
    paginate_by = 15
    success_url = reverse_lazy('home')
    extra_context = {
        'select_todas':'selected-nav',
        'action': success_url
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_form_valid = False

    def post(self, *args, **kwargs):
        self.is_form_valid = True
        self.form = form = self.get_form()
        return super().get(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        agora = date.today().replace(day=1)
        proximo_mes = agora.replace(month=agora.month+1)
        qs = super().get_queryset(*args, **kwargs).filter(
            conta_fk__usuario_fk = self.request.user,
        )

        mes = self.request.GET.get('mes', None)
        responsavel = self.request.GET.get('responsavel', None)

        if mes is not None:
            qs = qs.filter(mes__gt=agora, mes__lt=proximo_mes)

        if responsavel is not None:
            qs = qs.filter(conta_fk__responsavel__icontains=responsavel)
        
        if self.is_form_valid:
            qs = self.form.filter(qs)
        
        return qs.order_by('mes')

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['date'] = date.today()

        total = self.get_queryset().filter(
            pago=False
        ).aggregate(Sum('valor'))
        total_gasto = self.get_queryset().aggregate(Sum('valor'))

        context['total'] = total['valor__sum'] if total['valor__sum'] else 0 
        context['total_gasto'] = total_gasto['valor__sum'] if total_gasto['valor__sum'] else 0 
        context = { **context, **self.extra_context }
        return context


class EsteMesDividasListView(HomeListView):
    extra_context = {
        'select_este_mes':'selected-nav',
        'action': reverse_lazy('dividas-este-mes')
    }
    def get_queryset(self, *args, **kwargs):
        agora = date.today().replace(day=1)
        proximo_mes = agora.replace(month=agora.month+1)
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(mes__gt=agora, mes__lt=proximo_mes)


class DividasPagasListView(HomeListView):
    extra_context = {
        'select_pagas':'selected-nav',
        'action': reverse_lazy('dividas-pagas')
    }
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(pago=True)


class DividasEmAtrasoListView(HomeListView):
    extra_context = {
        'select_atraso':'selected-nav',
        'action': reverse_lazy('dividas-em-atraso')
    }
    def get_queryset(self, *args, **kwargs):
        agora = date.today().replace(day=1)
        proximo_mes = agora.replace(month=agora.month+1)
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(
            conta_fk__usuario_fk = self.request.user, 
            mes__lt=proximo_mes, pago=False
        )


class PayManyCheckboxView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect(reverse_lazy('home'))

    def post(self, request):
        ids = []
        data = request.POST['ids']
        if data:
            for i in data.split(','):
                ids.append(int(i))

            form = PayManyParcelaForm({'parcela_ids': ids})
            form.save()

        return redirect(reverse_lazy('home'))