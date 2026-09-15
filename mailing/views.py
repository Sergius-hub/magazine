from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Recipient, Message, Mailing
from .services import MailingService

class StatisticView(TemplateView):
    """Страница со статистикой по рассылкам."""

    template_name = "mailing/statistic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = MailingService.get_statistics()

        context["total_mailings"] = stats["total_mailings"]
        context["active_mailings"] = stats["active_mailings"]
        context["total_recipients"] = stats["total_recipients"]

        return context
