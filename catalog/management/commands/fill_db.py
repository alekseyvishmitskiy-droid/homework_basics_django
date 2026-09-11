from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Очищает базу данных и загружает новые тестовые данные'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()


        categories_data = [
            {'name': 'Электроника', 'description': 'Гаджеты, телефоны, ноутбуки'},
            {'name': 'Книги', 'description': 'Художественная и техническая литература'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'}
        ]


        created_categories = {}
        for cat_item in categories_data:
            category = Category.objects.create(**cat_item)
            created_categories[category.name] = category


        products_data = [
            {
                'name': 'Ноутбук',
                'description': 'Мощный игровой ноутбук',
                'price': 89990.00,
                'category': created_categories['Электроника']
            },
            {
                'name': 'Смартфон',
                'description': 'Флагман с отличной камерой',
                'price': 64990.00,
                'category': created_categories['Электроника']
            },
            {
                'name': 'Учебник по Django',
                'description': 'Полное руководство по веб-разработке',
                'price': 2500.00,
                'category': created_categories['Книги']
            }
        ]

        for prod_item in products_data:
            Product.objects.create(**prod_item)

        self.stdout.write(self.style.SUCCESS('База данных успешно очищена и заполнена тестовыми данными!'))
