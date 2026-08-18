from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy



from .models import Product
from .forms import ContactForm, ProductForm


# Просмотр
class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

# Детальный просмотр
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

# Создание продукта
class CreateProductView(CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy( "catalog:success" )

    def form_valid( self, form ):
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        image = form.cleaned_data["image"]
        price = form.cleaned_data["price"]
        category = form.cleaned_data["category"]
        #
        messages.success(
            self.request,
            f"Спасибо, продукт: {name} добавлен в базу."
        )

        return super().form_valid( form )

# Редактирование продукта
# class UpdateProductView(UpdateView):
#     model = Product
#     template_name = 'catalog/product_form.html'
#     form_class = ProductForm
#     success_url = reverse_lazy("catalog:success")

# Просмотр контактов и формы
class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy( "catalog:success" )

    def form_valid( self, form ):
        name = form.cleaned_data["name"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        print( name, phone, message )

        messages.success(
            self.request,
            f"Спасибо, {name}! Ваше сообщение отправлено."
        )

        return super().form_valid( form )

# Просмотр успешного шаблона
class SuccessView(TemplateView):
    template_name = 'catalog/success.html'
