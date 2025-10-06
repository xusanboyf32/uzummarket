from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from .product import Product

from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    RATING_CHOICES = [
        (1,"️️⭐️"),
        (2,"⭐️⭐️"),
        (3, "⭐️⭐️⭐️️️️️"),
        (4, "⭐️⭐️⭐️⭐️"),
        (5,"⭐️⭐️⭐️⭐️⭐️"),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"

# CHegirma
class FlashSale(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    # cost = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    # chegirma narxi bo'yicha chiqishi
    class Meta:
        unique_together = ('product','start_time', 'end_time')


class ProductViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-added_at"]
        verbose_name = "View History"
        verbose_name_plural = "View Histories"

    def __str__(self):
        return f"{self.user} -> {self.product}"


# Qo'shimcha vaqtinchalik savatcha
class Withlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-added_at"]
        verbose_name = "Withlist"
        verbose_name_plural = "Withlists"

    def __str__(self):
        return f"{self.user} -> {self.product}"



