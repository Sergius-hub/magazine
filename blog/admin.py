from django.contrib import admin
from .models import Record

# Register your models here.


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "content",
        "image",
        "created_at",
        "is_active",
        "count_views",
    )
