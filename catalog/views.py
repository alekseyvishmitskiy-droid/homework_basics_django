from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from catalog.services import get_products_by_category, get_all_published_products

class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Product.objects.all().order_by("-id")
            if self.request.user.has_perm('catalog.can_unpublish_product'):
                pass
            else:
                queryset = queryset.filter(Q(is_published=True) | Q(owner=self.request.user))
            return queryset


        return get_all_published_products()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_published:
            is_owner = obj.owner == self.request.user
            is_moderator = self.request.user.has_perm('catalog.can_unpublish_product')

            if not (is_owner or is_moderator):
                raise PermissionDenied("Этот продукт еще не прошел модерацию.")
        return obj


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        is_owner = obj.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.delete_product')

        if not (is_owner or is_moderator):
            raise PermissionDenied("У вас нет прав на удаление этого продукта.")
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

        context["success_message"] = "Данные успешно отправлены!"
        return self.render_to_response(context)


class ProductModerationView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductModeratorForm
    template_name = "catalog/product_form.html"
    permission_required = "catalog.can_unpublish_product"
    success_url = reverse_lazy("catalog:home")


class CategoryProductListView(ListView):
    """Отображение списка продуктов для конкретной категории с использованием низкоуровневого кэша."""
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category_pk = self.kwargs.get('pk')
        return get_products_by_category(self.category_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.category_pk)
        return context
