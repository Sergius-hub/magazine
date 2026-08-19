from django import forms
from django.forms.fields import BooleanField
from django.forms.widgets import Select
from .models import Record


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

class RecordForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Record
        fields = ("title", "content", "image", "is_active", "count_views")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Введите название блога",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Содержание",
                    "rows": 4,
                }
            ),
            "image": forms.ClearableFileInput(),
            "is_active": forms.CheckboxInput(),
            "count_views": forms.NumberInput(
                attrs={
                    "step": "1",
                    "placeholder": "0",
                }
            ),
        }

        labels = {
            "title": "Название",
            "content": "Содержание",
            "image": "Изображение",
            "is_active": "Активность",
            "count_views": "Количество просмотров",
        }
