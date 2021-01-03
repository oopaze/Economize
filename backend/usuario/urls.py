from django.urls import path
from .views import UserListView, UserPasswordChangeView, UserCreateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name="user-list"),
    path('add/', UserCreateView.as_view(), name="user-add"),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name="user-delete"),
    path('password/change/', UserPasswordChangeView.as_view(), name="user-password-change")
]