
from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from products.models.order import Order
from products.models.misc import Review
from products.models.product import  Category
from products.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from products.serializers.order import OrderSerializer
from products.serializers.misc import ReviewSerializer, CategorySerializer
#################################
# from products.models import ServiceLocation

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]  # Bunda permissionda object egasigina tahrirlay oladi qolganlar only read edi shuni qoysang keyin dasturda ishlaydi permit
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# IZOH
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # filter_backends = [filters.SearchFilter]
    search_fields = ['^name', '^description']


# yurakcha bosganda yoqtirganlarga qo'shish
from rest_framework import viewsets, permissions
from products.models.misc import Withlist
from products.serializers.misc import WithlistSerializer

class WithlistViewSet(viewsets.ModelViewSet):
    queryset = Withlist.objects.all()
    serializer_class = WithlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Withlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)

####################################################################
    # @action(detail=False, methods=['post'])
    # def toggle(self, request):
    #     product_id = request.data.get('product_id')
    #     if not product_id:
    #         return Response({'error': 'product_id required'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     product = get_object_or_404(Product, id=product_id)
    #     wishlist_item = Withlist.objects.filter(user=request.user, product=product).first()
    #
    #     if wishlist_item:
    #         wishlist_item.delete()
    #         return Response({'status': 'removed', 'in_wishlist': False})
    #     else:
    #         Wishlist.objects.create(user=request.user, product=product)
    #         return Response({'status': 'added', 'in_wishlist': True})
####################################################################



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models.product import Category, Product

@login_required
def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

@login_required
def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {'category': category, 'products': products})


@login_required
def wishlist_view(request):
    return render(request, 'products/wishlist.html')



@login_required
def checkout_view(request):
    return render(request, 'products/checkout.html')


