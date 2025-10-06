from django.db import models
from .product import Product
from django.conf import settings
from django.core.validators import RegexValidator # bunda malum bir formatadagi ma'lumotni tekshirish (kodda phone_number uchun)


phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be in the format: '+998xxxxxxxxx'"
)


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    is_paid = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"Order({self.product.name} by {self.customer.username})"



