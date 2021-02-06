from django.urls import path

from .views import (
    PayManyCheckboxView,
    DividasEmAtrasoListView,
    DividasPagasListView,
    HomeListView,
    EsteMesDividasListView
)
from .api import (
    ParcelasListView,
    ParcelaUpdateView,
    PayParcelaUpdateView
)

web_url = [
    #Dividas
    path('pay/many/', PayManyCheckboxView.as_view(), name='pay-many-parcela'),
    path('', HomeListView.as_view(), name='home'),
    path('este-mes/', EsteMesDividasListView.as_view(), name='dividas-este-mes'),
    path('pagas/', DividasPagasListView.as_view(), name='dividas-pagas'),
    path('em-atraso/', DividasEmAtrasoListView.as_view(), name='dividas-em-atraso'),
]

api_url = [
    path('api/parcelas/', ParcelasListView.as_view(), name='listar-parcelas'),
    path('api/parcela/<int:pk>/', ParcelaUpdateView.as_view(), name='editar-parcelas'),
    path('api/parcela/many/', PayParcelaUpdateView.as_view(), name='pagar-parcelas'),
]

urlpatterns = web_url + api_url
