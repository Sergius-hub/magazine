from django.db import models

# Create your models here.

class Recipient(models.Model):

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О",
        blank=True,
        null=True,
    )

    comments = models.TextField(
        verbose_name="Комментарии",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["id"]


class Message(models.Model):

    subject = models.CharField(
        max_length=150,
        verbose_name="Тема письма"
    )

    message = models.TextField(
        verbose_name="Тело писма"
    )


class Mailing(models.Model):

    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(
        auto_now_add=True,
    )

    end_time = models.DateTimeField(
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус публикации"
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )

    recipients = models.ManyToManyField(
        Recipient,
        related_name="mailings",
        verbose_name="Получатели",
        blank=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]

    def __str__( self ):
        return f"Рассылка от {self.start_time:%d.%m.%Y %H:%M}"

    def update_status(self, status):
        """
        Пересчитывает статус и сохраняет в БД, если он изменился.
        """
        pass

# mailings/models.py
class MailingAttempt(models.Model):
    """Запись о попытке отправки рассылки."""

    class Status(models.TextChoices):
        SUCCESS = "success", "Успешно"
        FAILED = "failed", "Не успешно"

    attempt_time = models.DateTimeField(
        "Дата и время попытки",
        auto_now_add=True,
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
    )
    server_response = models.TextField(
        "Ответ почтового сервера",
        blank=True,
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]

    def __str__(self):
        return f"Попытка {self.attempt_time:%d.%m.%Y %H:%M} — {self.get_status_display()}"

