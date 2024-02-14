from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField()
    stock = models.IntegerField()
    product_description = models.TextField(null=True)
    product_image = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):  # magic function
        return self.product_name
