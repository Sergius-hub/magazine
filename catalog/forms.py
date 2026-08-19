from django import forms
from django.forms import BooleanField
from django.forms.widgets import Select, RadioSelect, CheckboxSelectMultiple

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


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Введите название товара",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Введите описание товара",
                    "rows": 4,
                }
            ),
            "image": forms.ClearableFileInput(),
            "category": forms.Select(),
            "price": forms.NumberInput(
                attrs={
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
        name = self.cleaned_data.get("name").strip()
        if name.lower() in BLACK_LIST:
            raise ValidationError("Недопустимое название товара")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description").strip()
        if description.lower() in BLACK_LIST:
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
