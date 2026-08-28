from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "password",
        "first_name",
        "last_name",
        "last_login",
        "date_joined",
        "is_superuser",
        "is_staff",
        "is_active",
        "avatar",
        "phone",
        "country",
        "email",
    )