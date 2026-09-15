from django.utils import timezone

from .models import Mailing, Recipient

class MailingService:
    """Бизнес-логика сервиса рассылок."""

    @staticmethod
    def get_statistics() -> dict:
        """Статистика для страницы рассылок."""
        now = timezone.now()

        return {
            "total_mailings": Mailing.objects.count(),
            "active_mailings": Mailing.objects.filter(
                start_time__lte=now,
                end_time__gte=now,
                status=Mailing.STATUS_STARTED,
            ).count(),
            "total_recipients": Recipient.objects.count(),
        }
