from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .forms import AuthUserForm


class UserLoginView(LoginView):
    template_name = 'usuario/login.html'
    authentication_form = AuthUserForm


class UserLogoutView(RedirectView):
    url = reverse_lazy('web-login')

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)