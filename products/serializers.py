from rest_framework import serializers
from decimal import Decimal
from products.models import Category, Product, Review, ProductImage
from django.contrib.auth import get_user_model


class CategorySerializers(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField() 
    class Meta:
        model = Category
        fields = ['id','name','description','product_count']
        read_only_fields = ["product_count"]

    def get_product_count(self, obj):
        return Product.objects.filter(category=obj).count()
 
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage 
        fields = ['id','image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'category','price', 'price_with_tax','images']


    price_with_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    def calculate_tax(self,product):
        return round(product.price * Decimal(1.1), 2)
    

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_full_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user','product','rating', 'comment']
        read_only_fields = ['user','product']

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context['product_id']
        product = Product.objects.get(pk=product_id)
        review = Review.objects.create(product=product, **validated_data)
        return review 


