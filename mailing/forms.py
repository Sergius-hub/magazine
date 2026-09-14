from django import forms

from .models import Recipient
from catalog.mixins import StyleFormMixin

class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        feilds = ("email", "full_name", "comments")
        widgets = {

            "email": forms.TextInput(
                attrs={
                    "placeholder": "Укажите электронную почту для получения рассылки",
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Ф.И.О",
                }
            ),

            "comments": forms.Textarea(
                attrs={
                    "placeholder": "Комментарии",
                }
            ),
        }
