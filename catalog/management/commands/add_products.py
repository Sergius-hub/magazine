from django.core.management import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Добавление продуктов в базу данных"

    def handle(self, *args, **options):

        call_command("clear_tables")

        category, _ = Category.objects.get_or_create(
            name="Первая категория", description="Описание первой категории"
        )

        products = [
            {"name": "Ручка", "description": "Шариковая ручка", "category": category, "price": 5.00},
            {"name": "Карандаш", "description": "Деревянный карандаш", "category": category, "price": 7.00},
            {"name": "Стёрка", "description": "Резиновая стерка", "category": category, "price": 3.00},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Добавлен продукт: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Такой продукт уже добавлен:  {product.name}")
                )
