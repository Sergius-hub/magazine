from django.contrib import admin
from .models import Category, Product

# Register your models here.
# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "formatted_date",
        "category",
        "description",
        "price",
        "image",
    )
    list_filter = ("category",)
    search_fields = (
        "name",
        "description",
    )

    @admin.display(description="Дата создания", ordering="created_at")
    def formatted_date(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
