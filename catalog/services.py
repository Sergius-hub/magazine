from django.core.cache import cache
from .models import Product, Category


class ProductService:

    CACHE_TIMEOUT = 60 * 15

    @staticmethod
    def get_products_by_category(category_id: int):
        """Продукты определенной категории"""
        return (
            Product.objects
            .filter(category_id=category_id)
            .select_related('owner', 'category')
        )

    @staticmethod
    def get_products_by_category_cached(category_id: int) -> list:
        """С кэшем — для публичных страниц."""
        cache_key = f'products_by_category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            products = list(ProductService.get_products_by_category(category_id))
            cache.set(cache_key, products, ProductService.CACHE_TIMEOUT)

        return products

    @staticmethod
    def invalidate_category_cache(category_id: int) -> None:
        """Очистка кэша при изменении продуктов."""
        cache.delete(f'products_by_category_{category_id}')