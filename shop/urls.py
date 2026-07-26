
from django.urls import path
from shop.apps import ShopConfig
from shop.views import home, contacts

app_name = ShopConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]