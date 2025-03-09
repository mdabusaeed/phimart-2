from products.models import Product, Category, Review, ProductImage 
from products.serializers import ProductSerializer, CategorySerializers, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend 
from products.filters import ProductFilterSet
from rest_framework.filters import SearchFilter, OrderingFilter
from products.pagination import CustomPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissions
from products.permissions import IsReveiwAuthor


class ProductViewList(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    pagination_class = CustomPagination  
    search_fields = ['name','description', 'category__name']
    ordering_fields = ['price', 'stock']
    permission_classes = [IsAdminOrReadOnly]

    
class CategoryViewList(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializers


class ReviewViewList(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReveiwAuthor]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}  
    

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]
    def get_queryset(self):
        return  ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_pk'])
    
    
