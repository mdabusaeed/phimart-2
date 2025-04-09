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
from drf_yasg import openapi


class ProductViewList(ModelViewSet):
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
        operation_summary='Retrieve a list of products',
        operation_description='Filter and search products with various parameters',
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                description='Search term for product name or description',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                description='Field to order results (price, -price, updated_at etc.)',
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                description='Page number for pagination',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='price__gt',
                in_=openapi.IN_QUERY,
                description='Filter products with price greater than',
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                name='price__lt',
                in_=openapi.IN_QUERY,
                description='Filter products with price less than',
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                name='category_id',
                in_=openapi.IN_QUERY,
                description='Filter by exact category ID',
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: ProductSerializer(many=True),
            400: 'Bad Request'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
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
    
    
