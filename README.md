# magazine
Сайт магазина на Django

## Установка
```commandline
git clone https://github.com/Sergius-hub/magazine.git
```

## Flow работы

1) создание пользователя и бд в Postgress SQL:
CREATE USER user_name WITH PASSWORD 'password';
CREATE DATABASE db_name OWNER user_name;

2) создание моделей (таблицы) в приложении Django:
```Python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    price = models.FloatField(verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
```

3) Создание миграций в базу данных
python manage.py makemigrations
python manage.py migrate


4) Создаем суперпользователя для Админки (/admin/)
python manage.py createsuperuser
admin - f345678

5) Настраиваем админку(app_name/admin.py):
```Python
from django.contrib import admin
from .models import Category, Product

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("created_at", "category", "name", "description", "price", "image")
    list_filter = ("category",)
    search_fields = ("name", "description",)
``` 
6) python shell (использование):
poetry add ipython
python manage.py shell -i ipython

```shell
from catalog.models import Category, Product
all_products_2 = category2.products.all()
for product in category2.products.all():
    ...:     print(product.id, product.created_at, product.category.name, product.name, product.price, product.image)
Product.objects.filter(id=6).update(price=999.99)
Product.objects.get(name="Системный блок").delete()
for product in category2.products.all():
    ...:     print(product.id, product.created_at, product.category.name, product.name, product.price, product.image) 
```

7) Фикстуры Django shell:
Выгрузка:
python manage.py dumpdata [app_label].[model_name] --output [output_file] [additional_options]
python manage.py dumpdata catalog.product --output products_fixture.json
python -Xutf8 manage.py dumpdata catalog.product --output products_fixture.json --indent 4

Загрузка:
python manage.py loaddata products_fixture.json --format json

8) Кастомные функции:
add_products.py:
```Python
from django.core.management import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Добавление продуктов в базу данных'

    def handle(self, *args, **options):

        call_command( 'clear_tables' )

        category, _ = Category.objects.get_or_create(name="Первая категория", description = "Описание первой категории")

        products = [
            {"name": "Ручка", "category": category, "price": 5.00},
            {"name": "Карандаш", "category": category, "price": 7.00},
            {"name": "Стёрка", "category": category, "price": 3.00}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write( self.style.SUCCESS( f'Добавлен продукт: {product.name}' ) )
            else:
                self.stdout.write( self.style.WARNING( f'Такой продукт уже добавлен:  {product.name}' ) )
```

clear_tables.py
```
from django.core.management import BaseCommand
from django.db import connection


class Command( BaseCommand ):
    help = 'Очистка базы'

    def handle( self, *args, **options ):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;")

        self.stdout.write( self.style.SUCCESS( '✅ Таблицы очищены' ) )
```


9) Базовый шаблон:
Контент
```HTML
{% block content %}
    ...
{% endblock %}
```

Меню
```HTML
{% include 'includes/inc_menu.html' %}
```

Футер
```HTML
{% include 'includes/inc_footer.html' %}
```
