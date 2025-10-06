from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from products.models.product import Product
from products.models.misc import ProductViewHistory, FlashSale
from rest_framework import generics, serializers

from products.serializers.misc import FlashSaleSerializer
from django.utils import timezone

class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSaleSerializer

@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': "Product not found."}, status=status.HTTP_400_NOT_FOUND)
    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()
    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24),
        end_time__gte=timezone.now()

    ).first()
    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"This product will be on a {discount}% off flash sale!",
            "start_time":start_time,
            "end_time":end_time
        })
    else:
        return Response({
            "message": "No upcoming flash sales for this product"
        })



