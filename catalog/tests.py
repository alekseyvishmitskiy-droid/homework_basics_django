from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from catalog.models import Product, Category

User = get_user_model()


class UserAuthAndAccessTestCase(TestCase):

    def setUp(self):
        self.email = "testuser@example.com"
        self.password = "securepassword123"

        # Менеджер больше не требует username. Передаем только email и password.
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password
        )

        # Создаем обязательную тестовую категорию для исключения IntegrityError
        self.category = Category.objects.create(
            name="Тестовая категория",
            description="Описание тестовой категории"
        )

        # Создаем тестовый продукт с привязкой к категории и владельцу
        self.product = Product.objects.create(
            name="Тестовый товар",
            description="Описание",
            price=100,
            category=self.category,
            owner=self.user,
            is_published=True
        )

        # Настройка URL-маршрутов
        self.url_list = reverse("catalog:home")
        self.url_detail = reverse("catalog:product_detail", kwargs={"pk": self.product.pk})
        self.url_create = reverse("catalog:product_create")
        self.url_update = reverse("catalog:product_update", kwargs={"pk": self.product.pk})
        self.url_delete = reverse("catalog:product_delete", kwargs={"pk": self.product.pk})
        self.url_register = reverse("users:register")
        self.url_login = reverse("users:login")

    def test_successful_sequential_registrations(self):
        """Проверка двух последовательных регистраций по email без username"""
        emails = ["user_new1@example.com", "user_new2@example.com"]

        for email in emails:
            # Используем сложный уникальный пароль, чтобы пройти валидаторы Django
            secure_password = "SecurePass2026!#"

            response = self.client.post(
                self.url_register,
                {
                    "email": email,
                    "password": secure_password,
                    "password_confirm": secure_password,
                    "password1": secure_password,
                    "password2": secure_password,
                },
            )
            # В случае ошибки выводим контекст валидации формы
            form_errors = (
                response.context.get("form").errors
                if response.context and "form" in response.context
                else "Ошибки отсутствуют (успешный переход)"
            )
            self.assertEqual(
                response.status_code,
                302,
                msg=f"Регистрация не перенаправила пользователя. Ошибки формы: {form_errors}"
            )

        # Проверяем физическое присутствие пользователей в базе данных
        self.assertTrue(User.objects.filter(email="user_new1@example.com").exists())
        self.assertTrue(User.objects.filter(email="user_new2@example.com").exists())

        # Проверяем, что отправлено ровно 2 приветственных письма
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, "Добро пожаловать в наш интернет-магазин!")

    def test_login_by_email(self):
        """Проверка успешного входа на сайт по email через POST-запрос формы"""
        response = self.client.post(
            self.url_login,
            {
                "username": self.email,  # AuthenticationForm использует имя поля 'username' на HTML-странице
                "password": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_public_product_list_accessible(self):
        """Список товаров должен быть доступен без авторизации (код 200)"""
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_crud_redirects_anonymous_user(self):
        """Анонимный пользователь должен перенаправляться на страницу авторизации со всех страниц CRUD"""
        protected_urls = [self.url_detail, self.url_create, self.url_update, self.url_delete]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(settings.LOGIN_URL, response.url)

    def test_crud_accessible_by_authenticated_user(self):
        """Авторизованный пользователь должен успешно открывать защищенные страницы CRUD"""
        # Используем force_login для гарантированной имитации авторизации сессии в кастомной модели
        self.client.force_login(self.user)

        protected_urls = [self.url_detail, self.url_create, self.url_update, self.url_delete]

        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                200,
                msg=f"Авторизованный владелец получил статус {response.status_code} вместо 200 на URL: {url}"
            )
