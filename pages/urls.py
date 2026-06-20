from os import name

from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(
        template_name="form.html",
        extra_context={
            "heading": "Авторизация",
            "extra_link": "register",
            "extra_link_text": "Нет аккаунта? Содать",
            "submit_text": "Войти",
        }
    ), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("application/new/", views.application_create, name="application_create"),
    path("application/<int:application_id>/review/", views.review, name="review"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard")
]