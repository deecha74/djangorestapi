from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {
        "product": products,
    }
    return render(request, "product/index.html", context)


def post_product(request):
    # to insert products
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Product Added Successfully !"
            )
            return redirect("/products/addproduct/")
        else:
            messages.add_message(
                request, messages.ERROR, "Failed to add Product ! Please Verify "
            )
            return render(request, "/product/addproduct.html", {"forms": form})
        # to show add product form
    context = {
        "forms": ProductForm,
    }
    return render(request, "product/addproduct.html", context)


def post_category(request):
    # to insert products
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Category Added Successfully !"
            )
            return redirect("/products/addCategory/")
        else:
            messages.add_message(
                request, messages.ERROR, "Failed to add Category ! Please Verify "
            )
            return render(request, "/product/addCategory.html", {"forms": form})
        # to show add product form
    context = {
        "forms": CategoryForm,
    }
    return render(request, "product/addCategory.html", context)
