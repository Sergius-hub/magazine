from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

import datetime
import logging

from .forms import RegisterUserForm, LoginUserForm
from .models import User


logger = logging.getLogger(__name__)

class RegistrationView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy( "users:login" )

    def form_valid( self, form ):
        # Сохраняем пользователя
        response = super().form_valid(form)

        user = self.object

        # Автоматический вход
        login( self.request, user )

        # Отправляем приветственное письмо
        self.send_welcome_email( user )

        #
        return response

    def send_welcome_email( self, user ):
        """Отправить приветственное письмо. Не ломает регистрацию при ошибке."""
        now = datetime.datetime.now().strftime( "%Y-%m-%d %H:%M:%S" )
        message = f"""Здравствуйте, {user.username}!

        Спасибо за регистрацию в нашем сервисе.

        Ваши регистрационные данные:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Логин:    {user.username}
        Email:    {user.email}
        Телефон:  {user.phone or 'не указан'}
        Дата:     {now}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━

        С уважением,
        Команда сервиса
        """
        try:
            send_mail(
                subject="Добро пожаловать в наш сервис",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            # Логируем ошибку, но не прерываем регистрацию
            logger.error( f"Failed to send welcome email: {e}" )


class LoginUserView( LoginView ):
    template_name = "users/login.html"
    form_class = LoginUserForm
    redirect_authenticated_user = True

    def get_success_url( self ):
        return reverse_lazy( "catalog:home" )


