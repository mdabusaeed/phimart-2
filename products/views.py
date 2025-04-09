from products.models import Product, Category, Review, ProductImage 
from products.serializers import ProductSerializer, CategorySerializers, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend 
from products.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from products.pagination import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import DjangoModelPermissions
from products.permissions import IsReveiwAuthor
from drf_yasg.utils import swagger_auto_schema


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
     - Allows authenticated admin to create, update, and delete products
     - Allows users to browse and filter product
     - Support searching by name, description, and category
     - Support ordering by price and updated_at
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description','category__name']
    ordering_fields = ['price', 'updated_at', 'created_at']
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Retrive a list of products'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow an admin to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)

    
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
    
    
