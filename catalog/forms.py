from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")


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

