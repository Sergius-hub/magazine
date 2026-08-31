from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User"""
    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not email:
            raise ValueError("Email обязателен")

        # Нормализация email (приведение к нижнему регистру)
        email = self.normalize_email(email)

        # Создание пользователя
        user = self.model(email=email, **extra_fields)

        # Установка пароля с хэшированием
        user.set_password(password)

        # Сохранение в БД
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание суперпользователя"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """ Кастомная модель пользователя """
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Обязательное поле. Максимальная длина не более 150 символов. Только: буквы, цифры и @/./+/-/_.",
        error_messages={
            "unique": "Пользователь с таким именем уже существует.",
        },
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    avatar = models.ImageField(
        upload_to="images/users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )

    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Страна",
    )

    # Использование кастомного менеджера
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]

    def __str__(self):
        return self.email


