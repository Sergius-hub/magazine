from django import forms
from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ("title", "content", "image", "is_active", "count_views")

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название блога",
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Содержание",
                    "rows": 4,
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",

                }
            ),

            "count_views": forms.NumberInput(
                attrs={
                    "class": "form-control",
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