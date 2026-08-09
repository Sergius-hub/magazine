from django import forms
from .models import Product


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

class ContactForm(forms.Form):

    name = forms.CharField(
        max_length = 150,
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "name",
                "class": "form-control",
                "placeholder": "Ваше имя",
            }
        ),
    )

    phone = forms.CharField(
        max_length = 30,
        required=True,
        widget = forms.TextInput(
            attrs={
                "id": "phone",
                "type": "tel",
                "class": "form-control",
                "placeholder": "Контактный телефон",
            }
        )
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

