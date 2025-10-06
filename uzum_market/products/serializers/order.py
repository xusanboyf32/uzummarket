from django.contrib.auth import get_user_model # keyingi
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from products.models.order import Order, Product

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    customer = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'created_at', 'total_price', 'phone_number', 'is_paid',
                  'product_name']


    def get_total_price(self, obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        try:
            product_id = self.initial_data['product']
            product = Product.objects.get(id=product_id)

            if value > product.stock:
                raise serializers.ValidationError("Not enought items in stock")
            if value < 1:
                raise serializers.ValidationError("Quantity must be at least 1.")

            return value
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Product doesn't exist")

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        order = super().create(validated_data)
        order.product.stock -= order.quantity
        order.product.save()
        return order
