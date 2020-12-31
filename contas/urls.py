from django.urls import path
from .views import ContaCreateView, ContaListView, ContaDeleteView, ContaUpdateView

urlpatterns = [
    path('', ContaListView.as_view(), name='listar-contas'),
    path('add/', ContaCreateView.as_view(), name='create-conta'),
    path('edit/<int:pk>', ContaUpdateView.as_view(), name='update-conta'),
    path('delete/<int:pk>', ContaDeleteView.as_view(), name='deletar-conta'),
]