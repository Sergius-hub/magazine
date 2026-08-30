from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


from .apps import UsersConfig
from .views import RegistrationView, LoginUserView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginUserView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
]