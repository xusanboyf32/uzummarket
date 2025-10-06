# # from products.views.misc import CategoryViewSet, ReviewViewSet, OrderViewSet, WithlistViewSet
# # from products.views.product import ProductViewSet
# # # from . import signals
# #
# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from products.views.misc import location_view
# # from products.services import ProductViewHistoryCreate
# # from products.services import check_flash_sale, FlashSaleListCreateView
# # # from products.services import admin_replenish_stock
# # from .views import ProductViewSet, search_page
# #
# # router = DefaultRouter()
# # router.register(r'products',ProductViewSet)
# # router.register(r'reviews', ReviewViewSet)
# # router.register(r'categories', CategoryViewSet)
# # router.register(r'orders', OrderViewSet)
# # router.register(r'withlist', WithlistViewSet)
# #
# #
# # urlpatterns = [
# #     path('', include(router.urls)),
# #
# #     path('api/', include(router.urls)),
# #     path('search/', search_page, name='search_page'),
# #     path('api/products/autocomplete/', ProductViewSet.as_view({'get': 'autocomplete'}), name='autocomplete'),
# #
# #     ################################################
# #     path('sale/', FlashSaleListCreateView.as_view(), name='sale'),
# #     path('check-sale/<int:product_id>/', check_flash_sale, name='product-view-history-create'),
# #     path('product-view/', ProductViewHistoryCreate.as_view(), name='product-view-history-create'),
# #     # path('admin/replenish_stock/<int:product_id>/<int:amount>', admin_replenish_stock, name='admin_replenish_stock'),
# #     # path('cart/', cart_view, name='cart'),
# #     ###################################################
# #     # path('set-language/', views.set_language, name='set_language'),
# #     # path('search-products/', views.search_products, name='search_products'),
# #
# #     ###################################################
# #     path("location/", location_view, name="location"),
# #     # path('i18n/', include('django.conf.urls.i18n')),
# #
# #     # product_view_history
# #     path('product-view-history/', ProductViewHistoryCreate.as_view(), name='product-view-history'),
# #
# #
# # # path('products/<int:pk>/', product_detail_view, name='product_detail'),
# # # path('api/products/<int:pk>/like/', like_product, name='like_product'),
# # # path('api/cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
# #
# #
# #
# # ]
#
#
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from products.views.misc import (
#     OrderViewSet, ReviewViewSet, CategoryViewSet,
#     WithlistViewSet
# )
# from products.views.product import ProductViewSet
# from products.services.flash_sale import FlashSaleListCreateView, check_flash_sale
# from products.services.product_view_history import ProductViewHistoryCreate
#
# router = DefaultRouter()
# router.register(r'products', ProductViewSet, basename='product')
# router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'reviews', ReviewViewSet, basename='review')
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'wishlist', WithlistViewSet, basename='wishlist')
#
# urlpatterns = [
#     path('', include(router.urls)),
#
#     # Flash sale endpoints
#     path('flash-sales/', FlashSaleListCreateView.as_view(), name='flash-sales'),
#     path('products/<int:product_id>/check-flash-sale/', check_flash_sale, name='check-flash-sale'),
#
#     # Product view history
#     path('product-view-history/', ProductViewHistoryCreate.as_view(), name='product-view-history'),
#
#     # Product search and filters
#     path('products/autocomplete/', ProductViewSet.as_view({'get': 'autocomplete'}), name='product-autocomplete'),
#     path('products/search/', ProductViewSet.as_view({'get': 'search'}), name='product-search'),
#     path('products/top-rated/', ProductViewSet.as_view({'get': 'top_rated'}), name='top-rated-products'),
# ]
#
#

#######################################################

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.misc import (
    OrderViewSet, ReviewViewSet, CategoryViewSet, WithlistViewSet
)
from .views.product import ProductViewSet
from .services.flash_sale import FlashSaleListCreateView, check_flash_sale
from .services.product_view_history import ProductViewHistoryCreate

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'wishlist', WithlistViewSet, basename='wishlist')

urlpatterns = [
    # ==================== ROUTER URLs ====================
    path('', include(router.urls)),

    # ==================== ADDITIONAL API ENDPOINTS ====================
    path('flash-sale/', FlashSaleListCreateView.as_view(), name='flash-sale-list'),
    path('flash-sale/<int:product_id>/check/', check_flash_sale, name='check-flash-sale'),
    path('product-history/', ProductViewHistoryCreate.as_view(), name='product-history'),

    # ==================== SERVICE LOCATION ====================
    # path('locations/', include('products.urls_locations')),
]