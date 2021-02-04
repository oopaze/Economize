from django.urls import path
from .api import (
    ContaCreateView, 
    ContaListView, 
    ContaDeleteView, 
    ParcelasListView,
    ParcelaUpdateView,
    PayParcelaUpdateView
)
web_url = []

api_url = [
    ## Contas
    path('api/', ContaListView.as_view(), name='listar-contas'),
    path('api/add/', ContaCreateView.as_view(), name='create-conta'),
    path('api/delete/<int:pk>/', ContaDeleteView.as_view(), name='deletar-conta'),

    ## Contas Por Mês
    path('api/parcelas/', ParcelasListView.as_view(), name='listar-parcelas'),
    path('api/parcela/<int:pk>/', ParcelaUpdateView.as_view(), name='editar-parcelas'),
    path('api/parcela/many/', PayParcelaUpdateView.as_view(), name='pagar-parcelas'),
]

urlpatterns = web_url + api_url