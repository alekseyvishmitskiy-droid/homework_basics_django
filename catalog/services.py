from django.core.cache import cache
from config import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """Низкоуровневое кэширование списка опубликованных продуктов для конкретной категории."""
    if not settings.CACHES:
        return Product.objects.filter(category_id=category_id, is_published=True)

    key = f'products_category_{category_id}'
    products_list = cache.get(key)

    if products_list is None:
        products_list = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(key, products_list, timeout=600)  # Кэшируем на 10 минут

    return products_list



def get_all_published_products():
    """
    Низкоуровневое кэширование общего списка опубликованных продуктов.
    """
    if not settings.CACHES:
        return Product.objects.filter(is_published=True).order_by("-id")


    key = 'all_published_products'


    products_list = cache.get(key)


    if products_list is None:
        products_list = list(Product.objects.filter(is_published=True).order_by("-id"))
        cache.set(key, products_list, timeout=300)  # Кэшируем на 5 минут

    return products_list
