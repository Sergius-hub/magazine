from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import Select, RadioSelect, CheckboxSelectMultiple
from django.forms import BooleanField


from .models import User

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

class RegisterUserForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

        labels = {
            "username": "Никнейм",
            "email": "Электронная почта",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone": "Номер телефона",
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Пароль"
        self.fields["password1"].widget.attrs["placeholder"] = "Введите пароль"
        # self.fields["password1"].help_text = password_validation.password_validators_help_text_html()
        self.fields["password1"].help_text = """
                    <ul class="mb-0">
                        <li>Пароль не должен быть похож на вашу личную информацию.</li>
                        <li>Пароль должен содержать не менее 8 символов.</li>
                        <li>Пароль не может быть слишком распространённым.</li>
                        <li>Пароль не может состоять только из цифр.</li>
                    </ul>
                """


        self.fields["password2"].label = "Подтверждение пароля"
        self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"
        self.fields["password2"].help_text = "Для подтверждения введите тот же пароль, что и раньше."


class LoginUserForm( StyleFormMixin, AuthenticationForm ):
    """Кастомная форма входа со стилями Bootstrap."""

    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput( attrs={
            "placeholder": "Введите логин",
            "autofocus": True,
        } ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput( attrs={
            "placeholder": "Введите пароль",
        } ),
    )
