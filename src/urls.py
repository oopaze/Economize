from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('conta/', include("contas.urls"), name="contas"),
    path('api/v1/', include('api.urls'), name='api')
]