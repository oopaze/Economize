from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tabelas.models import Parcelamento
from .forms import PayManyParcelaForm, FilterParcelasForm


class HomeListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Parcelamento
    context_object_name = 'contas'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        agora = date.today().replace(day=1)
        proximo_mes = agora.replace(month=agora.month+1)# + relativedelta(month=+1)
        qs = super().get_queryset(*args, **kwargs).filter(
            conta_fk__usuario_fk = self.request.user
        )

        mes = self.request.GET.get('mes', None)
        pago = self.request.GET.get('pago', None)
        npago = self.request.GET.get('npago', None)
        responsavel = self.request.GET.get('responsavel', None)
        em_atraso = self.request.GET.get('em_atraso', None)

        if mes is not None:
            mes = datetime.strptime(mes, "%d/%m/%Y").date().replace(day=1)
            mes_proximo = mes.replace(month=mes.month + 1)
            qs = qs.filter(mes__gt=mes, mes__lt=mes_proximo)
        
        if em_atraso is not None:
            qs = super().get_queryset(*args, **kwargs).filter(
                conta_fk__usuario_fk = self.request.user, 
                mes__lt=agora, pago=False
            )

        if npago:
            qs = qs.filter(pago=False, mes__gt=agora, mes__lt=proximo_mes)
        
        elif pago:
            qs = qs.filter(pago=pago, mes__gt=agora, mes__lt=proximo_mes)
        
        if responsavel is not None:
            qs = qs.filter(conta_fk__responsavel__icontains=responsavel)
        
        return qs.order_by('mes')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['date'] = date.today()

        total = self.get_queryset().filter(
            pago=False
        ).aggregate(Sum('valor'))

        context['total'] = total['valor__sum'] if total['valor__sum'] else 0 
        context['filtro'] = FilterParcelasForm()

        return context


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