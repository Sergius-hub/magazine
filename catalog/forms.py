from django import forms
from .models import Product
from django.core.exceptions import ValidationError

BLACK_LIST = [
    "казино",
    "биржа",
    "обман",
    "криптовалюта",
    "дешево",
    "полиция",
    "крипта",
    "бесплатно",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название товара",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание товара",
                    "rows": 4,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "0.00",
                }
            ),
        }

        labels = {
            "name": "Название",
            "description": "Описание",
            "image": "Изображение",
            "category": "Категория",
            "price": "Цена",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name").strip().lower()
        if name in BLACK_LIST:
            raise ValidationError("Недопустимое название товара")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description").strip().lower()
        if description in BLACK_LIST:
            raise ValidationError("Недопустимое описание")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не должна быть отрицательной")
        return price


class ContactForm(forms.Form):

    name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "class": "form-control",
                "placeholder": "Ваше имя",
            }
        ),
    )

    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                "id": "phone",
                "type": "tel",
                "class": "form-control",
                "placeholder": "Контактный телефон",
            }
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "message",
                "class": "form-control",
                "placeholder": "Ваше сообщение",
                "rows": 5,
            }
        ),
    )
