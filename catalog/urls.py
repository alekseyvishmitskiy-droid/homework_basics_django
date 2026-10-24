from django.urls import path
from django.views.decorators.cache import cache_page 

from catalog.views import (
    ContactsTemplateView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    ProductDeleteView,
    ProductModerationView
)

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),


    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_detail"),

    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("products/<int:pk>/moderate/", ProductModerationView.as_view(), name="product_moderate"),
]
