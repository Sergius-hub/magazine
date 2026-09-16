from django.urls import path
from .apps import MailingConfig
from . import views

app_name = MailingConfig.name

urlpatterns = [
    # Главная
    path("mailing/", views.MailingView.as_view(), name="mailing"),

    # Рассылки
    path("mailings/", views.MailingListview.as_view(), name="mailing_list"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),


    # Получатели
    path("mailings/recipient/create/", views.RecipientCreateView.as_view(), name="recipient_create"),

    # Сообщения
    path("mailings/message/create/", views.MessageCreateView.as_view(), name="message_create"),
]