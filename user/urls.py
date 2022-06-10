from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("login-with-password/", views.LoginWithPassword.as_view()),
    path("message/", views.MessageView.as_view()),
]