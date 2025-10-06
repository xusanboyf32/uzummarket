import django_filters
from products.models.product import Product


class ProductFilter(django_filters.FilterSet):
    # Product nomi bo'yicha qidiruv
    name = django_filters.CharFilter(lookup_expr='icontains')

    # Brand nomi bo'yicha qidiruv
    brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'brand']


