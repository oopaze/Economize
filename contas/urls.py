from django.urls import path

from .views.contas import ContaCreateView, ContaListView, ContaDeleteView
from .views.parcelas import ParcelaListView


urlpatterns = [
    path('add/', ContaCreateView.as_view(), name="conta-create"),
    path('delete/<int:pk>/', ContaDeleteView.as_view(), name="conta-delete"),
    path('', ContaListView.as_view(), name="contas-list"),

    path('parcelas/', ParcelaListView.as_view(), name='parcelas-list'),
]