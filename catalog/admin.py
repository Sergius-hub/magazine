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
    list_display = ("created_at", "category", "name", "description", "price", "image")
    list_filter = ("category",)
    search_fields = ("name", "description",)