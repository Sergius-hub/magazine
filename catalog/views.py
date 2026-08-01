from django.shortcuts import render
from .models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "catalog/home.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return render(request, "catalog/success.html", {"name": name})
    return render(request, "catalog/contacts.html")
