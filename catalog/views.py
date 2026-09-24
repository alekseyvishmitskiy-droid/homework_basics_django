from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from catalog.forms import ProductForm
from catalog.models import Product



class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")


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



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")



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
