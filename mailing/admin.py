from django.contrib import admin

from .models import Mailing, Message, Recipient, MailingAttempt

class ReadOnlyAdminMixin:
    """Админка только для просмотра: без добавления, изменения и удаления."""

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        # все поля модели — только для чтения
        return [f.name for f in self.model._meta.fields]

# Админка для списка рассылок (Mailing)
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    # Список объектов в списке
    list_display = ('created_at', 'start_time', 'end_time', 'status', 'message', 'recipients_display')
    # Фильтр справа
    list_filter = ('status',)
    # Поиск по статусу
    search_fields = ('status', 'message')
    # Сортировка по умолчанию
    ordering = ('-created_at',)
    # Редактирование прямо в списке
    list_editable = ('start_time', 'end_time', 'status',)
    # Форма редактирования (то что отобразится при добавлении рассылки)
    fields = ('start_time', 'end_time', 'status', 'message', 'recipients')
    # Редактируемое отображение в списке (три электронные почты)
    @admin.display(description="Получатели")
    def recipients_display( self, obj ):
        recipients = obj.recipients.all()
        if not recipients:
            return "—"
        return ", ".join(r.email for r in recipients[:3])


# Админка для списка сообщений (Message)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Поля отображаемые в списке объектов
    list_display = ('subject', 'body')
    # Поиск по статусу
    search_fields = ('subject', 'body')
    # Сортировка по умолчанию
    ordering = ('-id',)


# Админка для получателя рассылки (Recipient)
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    # Поля отображаемые в списке объектов
    list_display = ('email', 'full_name', 'comments')
    # Поиск по статусу
    search_fields = ('email',)
    # Сортировка по умолчанию
    ordering = ('-id',)

# Админка для попыток отправки (MailingAttempt)
@admin.register(MailingAttempt)
class MailingAttemptAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    # Поля отображаемые в списке объектов
    list_display = ('attempt_time', 'status', 'server_response')

    # Сортировка по умолчанию
    ordering = ["-attempt_time"]

    # Навигация по датам
    date_hierarchy = "attempt_time"