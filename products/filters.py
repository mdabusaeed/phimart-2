from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter
from products.models import Product

class ProductFilter(FilterSet):
    # কাস্টম ফিল্টার ফিল্ড ডিফাইন করা
    price_min = NumberFilter(field_name='price', lookup_expr='gte', label='Minimum Price')
    price_max = NumberFilter(field_name='price', lookup_expr='lte', label='Maximum Price')
    category_name = CharFilter(field_name='category__name', lookup_expr='icontains', label='Category Name')
    search = CharFilter(field_name='name', lookup_expr='icontains', label='Product Name Search')

    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'price': ['gt', 'lt', 'gte', 'lte'],  # সবধরনের প্রাইস ফিল্টারিং
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ফিল্টার লেবেল কাস্টমাইজেশন
        self.filters['category_id'].label = 'Category ID (Exact Match)'
        self.filters['price__gt'].label = 'Price Greater Than'
        self.filters['price__lt'].label = 'Price Less Than'