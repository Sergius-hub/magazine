from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
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
    )

    filter_horizontal = ("groups", "user_permissions")

    # Поля для редактирования пользователя
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительно", {
            "fields": ("avatar", "phone", "country")
        }),
    )

    # Поля при создании пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {
            "fields": ("avatar", "phone", "country")
        }),
    )