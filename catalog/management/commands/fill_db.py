from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Очищает базу данных и корректно загружает тестовые данные из фикстур с сохранением связей'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Старт очистки базы данных...'))


        Product.objects.all().delete()
        Category.objects.all().delete()

        # Сбрасываем счетчики ID в PostgreSQL
        with connection.cursor() as cursor:
            try:
                cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")
                cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")
            except Exception:
                pass

        self.stdout.write(self.style.SUCCESS('База данных успешно очищена.'))


        self.stdout.write('Загрузка фикстур...')
        try:
            # Указываем точные названия файлов, которые лежат у вас в папке fixtures
            call_command('loaddata', 'category_data.json')
            call_command('loaddata', 'product_data.json')
            self.stdout.write(self.style.SUCCESS('Фикстуры успешно загружены!'))


            self.stdout.write(self.style.MIGRATE_LABEL('Проверка связей между моделями...'))
            products_count = Product.objects.count()
            categories_count = Category.objects.count()

            linked_correctly = True
            for product in Product.objects.all():
                if not product.category:
                    linked_correctly = False
                    self.stdout.write(self.style.ERROR(f'Ошибка: Продукт "{product.name}" потерял связь с категорией!'))

            if linked_correctly and products_count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'Проверка пройдена! Успешно загружено Категорий: {categories_count}, Продуктов: {products_count}. '
                    f'Все связи ForeignKey работают корректно.'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Критическая ошибка при импорте: {e}'))
