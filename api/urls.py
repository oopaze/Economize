from django.urls.conf import include
from contas.models import Conta
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ContaViewSet, ParcelaViewSet


app_name = "api"

router = DefaultRouter()
router.register(r'contas', ContaViewSet)
router.register(r'parcelas', ParcelaViewSet)

urlpatterns = [
    path('', include(router.urls), name="api-contas-list"),
]