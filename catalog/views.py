# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Product
# from .forms import ProductForm
#
# # Create your views here.
#
# def home(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, "catalog/home.html", context)
#
#
# def contacts(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#
#         return render(request, "catalog/success.html", {"name": name})
#     return render(request, "catalog/contacts.html")
#
#
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, "catalog/product_detail.html", context)
#
#
# def product_create(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             return redirect("catalog:product_detail", pk=product.pk)
#     else:
#         form = ProductForm()
#     return render(request, "catalog/product_form.html", {"form": form})

from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .models import Product
from .forms import ContactForm

class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


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

class SuccessView(TemplateView):
    template_name = 'catalog/success.html'
