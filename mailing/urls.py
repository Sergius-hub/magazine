from django.urls import path
from .apps import MailingConfig
from . import views

app_name = MailingConfig.name

urlpatterns = [
    # Статистика
    path("", views.StatisticView.as_view(), name="statistic"),

]