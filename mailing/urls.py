from django.urls import path
from .apps import MailingConfig
from . import views

app_name = MailingConfig.name

urlpatterns = [
    # Главная
    path("mailing/", views.MailingView.as_view(), name="mailing"),

    # Рассылки
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
]