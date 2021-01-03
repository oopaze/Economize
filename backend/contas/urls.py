from django.urls import path
from .views import (
    ContaCreateView, 
    ContaListView, 
    ContaDeleteView, 
    ParcelasListView,
    ParcelaUpdateView
)

urlpatterns = [
    ## Contas
    path('', ContaListView.as_view(), name='listar-contas'),
    path('add/', ContaCreateView.as_view(), name='create-conta'),
    path('delete/<int:pk>/', ContaDeleteView.as_view(), name='deletar-conta'),

    ## Contas Por Mês
    path('parcelas/', ParcelasListView.as_view(), name='listar-parcelas'),
    path('parcela/<int:pk>/', ParcelaUpdateView.as_view(), name='editar-parcelas'),
]