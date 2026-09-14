from django.contrib import admin

from .models import Mailing

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'message', 'recipients_display')

    @admin.display(description="Получатели")
    def recipients_display( self, obj ):
        recipients = obj.recipients.all()
        if not recipients:
            return "—"
        return ", ".join(r.email for r in recipients[:3])
