from django.db import models
from django.contrib.auth.models import User
from django.utils.module_loading import autodiscover_modules


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/',blank=True, null=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # chegirma foizi
    discount_price = models.PositiveIntegerField(null=True, blank=True, verbose_name="Chegirma narxi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    # image = models.ImageField(upload_to="products/images/")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity >self.stock:
            return "Omborda bu mahsulot mavjud emas"
        self.stock -= quantity
        self.save()

    def inscrease_stock(self, amount):
        self.stock += amount
        self.save()

        class Meta:
            # ordering = ['name']
            ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return f"Image for {self.product.name}"


