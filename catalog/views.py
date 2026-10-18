from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")


        if self.request.user.is_authenticated:
            if self.request.user.has_perm('catalog.can_unpublish_product'):
                pass
            else:
                queryset = queryset.filter(Q(is_published=True) | Q(owner=self.request.user))
        else:
            queryset = queryset.filter(is_published=True)


        latest_products = queryset[:5]
        print("\n--- ПОСЛЕДНИЕ 5 ПРОДУКТОВ В БАЗЕ ДАННЫХ (CBV) ---")
        for product in latest_products:
            print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
        print("-------------------------------------------------\n")

        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_published:
            if not self.request.user.is_authenticated:
                raise PermissionDenied("Этот продукт еще не прошел модерацию.")

            is_owner = obj.owner == self.request.user
            is_moderator = self.request.user.has_perm('catalog.can_unpublish_product')

            if not (is_owner or is_moderator):
                raise PermissionDenied("Этот продукт еще не прошел модерацию.")
        return obj


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта с автоматической привязкой владельца."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта. Доступно только владельцу."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)


        if obj.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта, редактирование запрещено.")

        return obj


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта. Доступно владельцу и модераторам."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)


        is_owner = obj.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator):
            raise PermissionDenied("У вас нет прав на删除 этого продукта.")

        return obj


class ContactsTemplateView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["success_message"] = None
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(f"Новая заявка! Имя: {name}, Телефон: {phone}, Сообщение: {message}")

        context["success_message"] = "Данные успешно отправлены!"

        return self.render_to_response(context)


class ProductModerationView(PermissionRequiredMixin, UpdateView):
    """Контроллер для модератора для изменения статуса публикации."""
    model = Product
    form_class = ProductModeratorForm
    template_name = "catalog/product_form.html"
    permission_required = "catalog.can_unpublish_product"
    success_url = reverse_lazy("catalog:home")
