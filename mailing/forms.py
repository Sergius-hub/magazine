from django import forms

from .models import Recipient, Message, Mailing
from catalog.mixins import StyleFormMixin

class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ("email", "full_name", "comments")
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
                    "rows": 3,
                }
            ),
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body")
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "placeholder": "Укажите тему письма",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Текст письма",
                    "rows": 6,
                }
            ),
        }

class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ("start_time", "end_time", "message", "recipients")
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "message": forms.Select(),
            "recipients": forms.SelectMultiple(
                attrs={
                    "size" : 8,
                }
            ),
        }

