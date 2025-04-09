from products.models import Product
from django_filters.rest_framework import FilterSet
from rest_framework.filters import SearchFilter, OrderingFilter



class ProductFilterSet(FilterSet):
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product 
        fields = {
            'category_id': ['exact'],
            # 'price' is not needed here since we are defining price_gt and price_lt explicitly
        }
        

# class ProductFilterSet(FilterSet):
#     class Meta:
#         model = Product 
#         fields = {
#             'category_id': ['exact'],
#             'price': ['gt', 'lt'],
#         }