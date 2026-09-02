from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse


from .models import Product
from .forms import ContactForm, ProductForm


# Просмотр
class ProductsListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


# Детальный просмотр
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


# Создание продукта
class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "catalog/product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:success")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        image = form.cleaned_data["image"]
        price = form.cleaned_data["price"]
        category = form.cleaned_data["category"]
        #
        messages.success(self.request, f"Спасибо, продукт: {name} добавлен в базу.")

        return super().form_valid(form)


# Редактирование продукта
class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "catalog/product_form.html"
    form_class = ProductForm
    # success_url = reverse_lazy("catalog:success")

    def form_valid(self, form):
        # Проверка прав
        user = self.request.user
        original_status = self.object.status
        new_status = form.cleaned_data.get("status")


        # Если нет права can_publish_product — блокируем ВСЁ
        if not user.has_perm('catalog.can_unpublish_product'):
            form.add_error("status", "У вас нет прав на изменение статуса")
            return self.form_invalid(form)

        # Если право есть — можно только на STATUS_ARCHIVED
        if new_status != self.model.STATUS_ARCHIVED:
            form.add_error("status", "Вы можете только архивировать продукт")
            return self.form_invalid(form)

        name = form.cleaned_data.get("name")

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        # print(name)

        messages.success(self.request, f"{name} успешно обновлен")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.object.pk])

# Удаление продукта
class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")


# Просмотр контактов и формы
class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:success")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]

        # Здесь можно отправить письмо, сохранить в файл,
        # отправить данные в Telegram, CRM и т.д.
        print(name, phone, message)

        messages.success(self.request, f"Спасибо, {name}! Ваше сообщение отправлено.")

        return super().form_valid(form)


# Просмотр успешного шаблона
class SuccessView(TemplateView):
    template_name = "catalog/success.html"
