import datetime

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm
from .models import User

class RegistrationView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy( "users:login" )

    def form_valid( self, form ):
        # Сохраняем пользователя (один раз!)
        user = form.save()

        # Автоматический вход
        login( self.request, user )

        # Отправляем приветственное письмо (безопасно)
        self.send_welcome_email( user.email )

        # Редирект (без повторного сохранения)
        return super().form_valid( form )

    def send_welcome_email( self, user_email ):
        """Отправить приветственное письмо. Не ломает регистрацию при ошибке."""
        now = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S" )
        try:
            send_mail(
                subject="Добро пожаловать в наш сервис",
                message=f"Спасибо, что зарегистрировались в нашем сервисе!\nВремя: {now}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=True,  # ← не падать при ошибке SMTP
            )
        except Exception as e:
            # Логируем ошибку, но не прерываем регистрацию
            import logging
            logging.getLogger( __name__ ).error( f"Failed to send welcome email: {e}" )


class LoginUserView( LoginView ):
    template_name = "users/login.html"
    form_class = LoginUserForm
    redirect_authenticated_user = True

    def get_success_url( self ):
        return reverse_lazy( "catalog:home" )


