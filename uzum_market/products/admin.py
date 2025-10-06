
from django.contrib import admin

from products.models import FlashSale
from products.models.product import Category, Product
from products.models.misc import Review
from products.models.order import Order
# from .models import ServiceLocation

from django.contrib import admin
from .models import ProductImage


#  BU ADMIN PANELGA REGISTRASIYA(ADMIN PANELDA KO'RINISHI UCHUN) PRO KODLAR
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("id",)
    list_filter = ("name",)


#################
from django.contrib import admin

class ProductImageInline(admin.TabularInline):
    model =ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock","created_at")
    list_filter = ("category", "created_at")  # filter paneli
    search_fields = ("name", "category__name")
    ordering = ("id",)
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")

#######################


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "date_posted")
    list_filter = ("rating", "date_posted")
    search_fields = ("product__name", "user__username")
    ordering = ("-date_posted",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "product", "quantity", "is_paid", "phone_number", "is_paid", "created_at")
    list_filter = ("is_paid", "created_at")
    search_fields = ("customer__username", "customer__email", "phone_number")
    ordering = ("-created_at",)



@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage', 'start_time', 'end_time', 'is_active')
    list_filter = ('start_time', 'end_time')
    search_fields = ('product__name',)





