from django.urls import path
from .views import index, post_product, post_category  # use * to import all


urlpatterns = [
    path("", index),
    path("addproduct/", post_product),
    path("addCategory/", post_category),
]
