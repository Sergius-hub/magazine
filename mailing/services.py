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

    @staticmethod
    def send_mailing( mailing: Mailing ) -> tuple:
        """Отправка одной рассылки с логированием попыток."""
        now = timezone.now()

        if not (mailing.start_time <= now <= mailing.end_time):
            return False, "Текущее время вне окна рассылки"

        recipients = mailing.recipients.all()
        if not recipients.exists():
            return False, "У рассылки нет получателей"

        sent = 0
        failed = 0

        for client in recipients:
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.STATUS_SUCCESS,
                    server_response=f"OK: {client.email}",
                )
                sent += 1

            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.STATUS_FAILED,
                    server_response=f"Ошибка: {str( e )}",
                )
                failed += 1

        return True, f"Отправлено: {sent}, ошибок: {failed}"