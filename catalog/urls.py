from django.urls import path

from .views import (
    ProductsListView,
    ProductDetailView,
    ContactsView,
    SuccessView,
    CreateProductView,
    UpdateProductView,
    DeleteProductView,
)
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductsListView.as_view(), name="home"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("success/", SuccessView.as_view(), name="success"),
    path("products/create/", CreateProductView.as_view(), name="product_create"),
    path(
        "products/<int:pk>/update/", UpdateProductView.as_view(), name="product_update"
    ),
    path(
        "products/<int:pk>/delete/", DeleteProductView.as_view(), name="product_delete"
    ),
]
