from django.urls import path
from .api import UserListView, UserPasswordChangeView, UserCreateView, UserDeleteView


urlpatterns = [
    path('api/', UserListView.as_view(), name="user-list"),
    path('api/add/', UserCreateView.as_view(), name="user-add"),
    path('api/delete/<int:pk>/', UserDeleteView.as_view(), name="user-delete"),
    path('api/password/change/', UserPasswordChangeView.as_view(), name="user-password-change")
]