from xmlrpc.client import Fault

import django_filters
from django.db import models
from django_filters import rest_framework as django_filters
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.filters import ProductFilter
from unicodedata import category

from products.models.product import Product
from products.permissions import IsStaffOrReadOnly
from products.serializers.misc import ProductSerializer
from django.db.models import Q
from xmlrpc.client import Fault


class CustomPagination(PageNumberPagination):
    page_size = 5


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description','category__name','tags__name', 'seller_shop_name']


    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category', None)
        if category:
            self.queryset = self.queryset.filter(category=category)
        return super().list(request, *args, **kwargs)

# u va unga oxshashlarini olib keladi
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        related_products = Product.objects.filter(category=instance.category).exclude(id=instance.id)[:5]
        related_serializers = ProductSerializer(related_products, many=True)
        return Response({
            'product':serializer.data,
            'related_products':related_serializers.data
        })


    # REAL TIME SEARCH
    @action(detail=False,methods=['get'])
    def autocomplete(self,request):
        query = request.query_params.get('q', '').strip().lower()

        # Faqat 1 ta harf terilsa ham ishlaydi
        if len(query) < 1:
            return Response([])

        # Barcha fieldlarda qidirish
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(seller__shop_name__icontains=query)
        ).select_related('category', 'seller').distinct()[:10]

        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'category': product.category.name,
                'price': str(product.price),
                'image': product.image.url if product.image else None,
                'type': 'product'
            })

        return Response(results)

# TO'LIQ SEARCH RESULTS
    @action(detail=False, methods=['get'])
    def search(self,request):
        query = request.query_params.get('q', '').strip()
        category_id = request.query_params.get('category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        products = self.get_queryset()
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(seller__shop_name__icontains=query)
            ).distinct()

        # Filterlar
        if category_id:
            products = products.filter(category_id=category_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

