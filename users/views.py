from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm
from .models import User

class RegistrationView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy( "catalog:home" )

