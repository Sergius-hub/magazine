from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


from .apps import UsersConfig
from .views import RegistrationView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
]