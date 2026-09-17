from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import MailingForm, RecipientForm, MessageForm
from .models import Mailing, Recipient, Message
from .services import MailingService

class MailingView(TemplateView):
    """Рендерит страницу со статистикой по рассылкам."""

    template_name = "mailing/mailing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = MailingService.get_statistics()

        context["total_mailings"] = stats["total_mailings"]
        context["active_mailings"] = stats["active_mailings"]
        context["total_recipients"] = stats["total_recipients"]

        return context



# CRUD - mailing
class MailingCreateView(CreateView):
    """Добавление новой рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mailing")

class MailingListview(ListView):
    """Просмотр списка рассылок."""
    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        return (
            super().get_queryset()
            .annotate(recipients_count=Count("recipients", distinct=True))
        )

class MailingUpdateView(UpdateView):
    """Редактирование рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_list")

class MailingDeleteView(DeleteView):
    """Удаление рассылки."""
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mailing_list")

# C - Recipient
class RecipientCreateView(CreateView):
    """Добавление нового получателя."""
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mailing")

# C - Message
class MessageCreateView(CreateView):
    """Добавление нового сообщения для рассылки."""
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mailing")

# Отправка
class SendMailingView(View):
    """Отправка одной рассылки."""

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.update_status()

        success, message = MailingService.send_mailing(mailing)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

        return redirect("mailing:mailing_list")