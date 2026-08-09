# from django.urls import path
# from catalog.apps import CatalogConfig
# from catalog.views import home, contacts, product_detail, product_create
#
# app_name = CatalogConfig.name
#
# urlpatterns = [
#     path("", home, name="home"),
#     path("contacts/", contacts, name="contacts"),
#     path("products/create/", product_create, name="product_create"),
#     path("products/<int:pk>/", product_detail, name="product_detail"),
# ]

from django.urls import path

from .views import ProductsListView, ProductDetailView, ContactsView, SuccessView, CreateProductView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductsListView.as_view(), name="home"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("success/", SuccessView.as_view(), name="success"),
    path( "products/create/", CreateProductView.as_view(), name="product_create" ),
]