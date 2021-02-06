from django.urls import path
from .api import (
    ContaCreateView, 
    ContaListView, 
    ContaDeleteView, 
)
from .views import (
    ContaListView
)


web_url = [
    path('', ContaListView.as_view(), name="contas-list"),
]

api_url = [
    ## Contas
    path('api/', ContaListView.as_view(), name='listar-contas'),
    path('api/add/', ContaCreateView.as_view(), name='create-conta'),
    path('api/delete/<int:pk>/', ContaDeleteView.as_view(), name='deletar-conta'),
]

urlpatterns = web_url + api_url