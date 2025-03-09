from products.models import Product
from django_filters.rest_framework import FilterSet

class ProductFilterSet(FilterSet):
    class Meta:
        model = Product 
        fields = {
            'category_id': ['exact'],
            'price': ['gt', 'lt'],
        }
        