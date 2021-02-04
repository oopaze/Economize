from django.urls import path

from .views import (
    PayManyCheckboxView,
    DividasEmAtrasoListView,
    DividasPagasListView,
    HomeListView,
    EsteMesDividasListView
)

web_url = [
    #Dividas
    path('pay/many/', PayManyCheckboxView.as_view(), name='pay-many-parcela'),
    path('', HomeListView.as_view(), name='home'),
    path('este-mes/', EsteMesDividasListView.as_view(), name='dividas-este-mes'),
    path('pagas/', DividasPagasListView.as_view(), name='dividas-pagas'),
    path('em-atraso/', DividasEmAtrasoListView.as_view(), name='dividas-em-atraso'),
]

api_url = []

urlpatterns = web_url + api_url
