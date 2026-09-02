from django.db import models
from users.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["id"]


class Product(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Черновик"),
        (STATUS_PUBLISHED, "Опубликован"),
        (STATUS_ARCHIVED, "В архиве"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to="images/product/", verbose_name="Изображение")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменение")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="Статус публикации"
    )

    def __str__(self):
        return f"{self.name}"

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["id"]
        permissions = [
            ("can_unpublish_product","может отменять публикацию продукта"),
        ]
