from django.urls import path

from catalog.views import (
    ContactsTemplateView,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    ProductDeleteView
)

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsTemplateView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),


    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
