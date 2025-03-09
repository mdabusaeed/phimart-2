from django.urls import path, include
from products.views import ProductViewList, CategoryViewList, ReviewViewList, ProductImageViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', ProductViewList, basename='products')
router.register('categories', CategoryViewList)
router.register('carts', CartViewSet, basename='carts',)
router.register('orders', OrderViewSet, basename='orders') 


product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewList, basename='product-reviews')
product_router.register('images', ProductImageViewSet, basename = 'product-image')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-item')
 

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(carts_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


