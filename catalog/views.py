from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
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

from .services import ProductService
from .models import Product, Category
from .forms import ContactForm, ProductForm
from .mixins import OwnerOrModeratorRequiredMixin, OwnerRequiredMixin

# Просмотр
class ProductsListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

# Просмотр по категории

class CategoryListView(ListView):
    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "categories"

class CategoryProductsView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, pk=self.kwargs['pk']
        )
        return ProductService.get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

# Детальный просмотр
@method_decorator(cache_page(60 * 15), name='dispatch')
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
        # Привязываем текущего пользователя к продукту ДО сохранения
        form.instance.owner = self.request.user

        name = form.cleaned_data["name"]
        description = form.cleaned_data["description"]
        image = form.cleaned_data["image"]
        price = form.cleaned_data["price"]
        category = form.cleaned_data["category"]
        #
        messages.success(self.request, f"Спасибо, продукт: {name} добавлен в базу.")

        return super().form_valid(form)


# Редактирование продукта
class UpdateProductView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
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
class DeleteProductView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    moderator_permission = 'catalog.delete_product'

    def form_valid(self, form):
        # Запоминаем имя до удаления
        product_name = self.object.name

        # Выполняем стандартное удаление
        response = super().form_valid(form)

        # Показываем сообщение
        messages.success(self.request, f"Продукт '{product_name}' удалён")
        return response

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
