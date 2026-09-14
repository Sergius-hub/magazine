from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Recipient(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    full_name = models.CharField(
        max_length=150,
        verbose_name="Ф.И.О",
        blank=True,
    )

    comments = models.TextField(
        verbose_name="Комментарии",
        blank=True,
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["-id"]


class Message(models.Model):
    """Модель сообщения"""
    subject = models.CharField(
        max_length=150,
        verbose_name="Тема письма"
    )

    body = models.TextField(
        verbose_name="Тело письма"
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-id"]

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    """Модель рассылки"""
    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_FINISHED = "finished"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(
        "Дата и время начала",
    )

    end_time = models.DateTimeField(
        "Дата и время окончания",
    )

    created_at = models.DateTimeField(
        verbose_name="Создана",
        auto_now_add=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус рассылки"
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

    def __str__(self):
        return f"Рассылка от {self.start_time:%d.%m.%Y %H:%M}"

    def update_status(self):
        """
        Пересчитывает статус и сохраняет в БД, если он изменился.
        """
        now = timezone.now()
        new_status = None

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif now <= self.end_time:
            new_status = self.STATUS_STARTED
        else:
            new_status = self.STATUS_FINISHED

        if new_status and self.status != new_status:
            self.status = new_status
            # Сохраняем только поле статуса, не трогая остальные
            self.save(update_fields=["status"])

        return self.status

    def clean(self):
        """
        Валидация на уровне модели.
        Вызывается при использовании ModelForm и в админке.
        """
        super().clean()

        now = timezone.now()

        # Проверка 1: start_time не может быть в прошлом
        if self.start_time and self.start_time < now:
            raise ValidationError(
                "Дата начала рассылки не может быть в прошлом"
            )

        # Проверка 2: start_time должен быть раньше end_time
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    "Дата начала должна быть раньше даты окончания"
                )


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

