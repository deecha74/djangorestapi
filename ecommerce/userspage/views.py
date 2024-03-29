from django.shortcuts import render, redirect
from product.models import Product, Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from product.forms import OrderForm
from product.models import Order
from django.views import View
from django.urls import reverse


# Create your views here.


def index(request):
    products = Product.objects.all().order_by("-id")[:8]
    context = {"products": products}

    return render(request, "users/index.html", context)


def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {"product": product}

    return render(request, "users/productdetails.html", context)


def products(request):
    products = Product.objects.all().order_by("-id")
    context = {"products": products}

    return render(request, "users/products.html", context)


# to register user


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Account Created")
            return redirect("/register")

        else:
            messages.add_message(request, messages.ERROR, "Please Verify the fields ")
            return render(request, "users/register.html", {"forms": form})

    context = {"forms": UserCreationForm}
    return render(request, "users/register.html", context)


# login processor


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("/admin/dashboard")
                else:
                    return redirect("/")

            else:
                messages.add_message(
                    request, messages.ERROR, "Please Provide correct Credentials"
                )
                return render(request, "users/login.html", {"forms": form})
    context = {"forms": LoginForm}
    return render(request, "users/login.html", context)


# logout
def logout_user(request):
    logout(request)
    return redirect("/login")


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    check_item_presense = Cart.objects.filter(user=user, product=product)
    if check_item_presense:
        messages.add_message(request, messages.ERROR, "Product is already in the cart ")
        return redirect("/cart")

    else:
        cart = Cart.objects.create(product=product, user=user)
        if cart:
            messages.add_message(request, messages.SUCCESS, "Product added to cart")
            return redirect("/cart")
        else:
            messages.add_message(request, messages.ERROR, "Failed to load")


@login_required
def show_user_cart_items(request):
    user = request.user
    items = Cart.objects.filter(user=user)
    context = {"items": items}
    return render(request, "users/cart.html", context)


@login_required
def remove_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.add_message(request, messages.SUCCESS, "Item Removed from the cart ")
    return redirect("/cart")


@login_required
def post_order(request, product_id, cart_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.get(id=cart_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = request.POST.get("quantity")
            price = product.product_price
            total_price = int(quantity) * int(price)
            contact_no = request.POST.get("contact_no")
            address = request.POST.get("address")
            payment_method = request.POST.get("payment_method")
            payment_status = request.POST.get("payment_status")
            # to create an order
            order = Order.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                total_price=total_price,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
                payment_status=payment_status,
            )
            if order.payment_method == "Cash on Delivery":
                cart_item.delete()
                messages.add_message(request, messages.SUCCESS, "Order Successful")
                return redirect("/myorder")
            elif order.payment_method == "E-sewa":
                context = {
                    "order": order,
                    "cart": cart_item,
                }
                return (
                    redirect(
                        reverse("esewaform")
                        + "?o_id="
                        + str(order.id)
                        + "c_id"
                        + str(cart_item.id)
                    )
                    + "c_id"
                    + str()
                )

            else:
                messages.add_message(request, messages.ERROR, "Failed to make an order")
                return render(request, "users/orderform.html", {"forms": form})

    context = {"forms": OrderForm}
    return render(request, "users/orderform.html", context)


import requests as req


# def esewa_verify(request):
#     import xml.etree.ElementTree as ET

#     o_id = request.GET.get("pid")
#     amount = request.GET.get("amt")
#     refID = request.GET.get("refID")
#     url = "https://uat.esewa.com.np/epay/transrec"
#     d = {
#         "amt": 100,
#         "scd": "EPAYTEST",
#         "rid": "000AE01",
#         "pid": "ee2c3ca1-696b-4cc5-a6be-2c40d929d453",
#     }
#     resp = req.post(url, d)
#     root = ET.fromstring(resp.content)
#     status = root[0].text.strip()

#     if status == "Success":
#         order_id = o_id.split("_")[0]
#         order = Order.objects.get(id=order_id)
#         order.payment_status = True
#         order.save()
#         # cart
#         cart_id = o_id.split("_")[0]
#         cart = Cart.objects.get(id=cart_id)
#         cart.delete()
#         messages.add_message(request, messages.SUCCESS, "Payment Successful ")
#         return redirect("/cart")
#     else:
#         messages.add_message(request, messages.ERROR, "Unable to make Payment ")
#         return redirect("/cart")


@login_required
def my_order(request):
    user = request.user
    items = Order.objects.filter(user=user)
    context = {"items": items}
    return render(request, "users/myorder.html", context)


import hmac
import hashlib
import uuid
import base64

import requests as req


class EsewaView(View):
    def get(self, request, *args, **kwargs):

        o_id = request.GET.get("o_id")
        c_id = request.GET.get("c_id")
        cart = Cart.objects.get(id=c_id)
        order = Order.objects.get(id=o_id)

        uuid_val = uuid.uuid4()

        def genSha256(key, message):
            key = key.encode("utf-8")
            message = message.encode("utf-8")
            hmac_sha256 = hmac.new(key, message, hashlib.sha256)
            digest = hmac_sha256.digest()
            signature = base64.b64encode(digest).decode("utf-8")
            return signature

        secret_key = "8gBm/:&EnhH.1/q"
        data_to_sign = f"total_amount={order.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"
        result = genSha256(secret_key, data_to_sign)

        data = {
            "amount": order.product.product_price,
            "total_amount": order.total_price,
            "transaction_uuid": uuid_val,
            "signature": result,
        }
        context = {"order": order, "data": data, "cart": cart}
        return render(request, "users/esewa_payment.html", context)


import json


@login_required
def esewaverify(request, order_id, cart_id):
    if request.method == "GET":
        data = request.GET.get("data")
        decoded_data = base64.b64decode(data).decode("utf-8")
        map_data = json.load(decoded_data)
        order = Order.objects.get(id=order_id)
        cart = Cart.objects.get(id=cart_id)

        if map_data.get("status") == "COMPLETE":
            order.payment_status = True
            order.save()
            cart.delete()
            messages.add_message(request, messages.SUCCESS, "Payment Successful")
            return redirect("/myorder")

        else:
            messages.add_message(request, messages.ERROR, "Payment Failed")
            return redirect("/myorder")
