from rest_framework.serializers import ModelSerializer
from .models import Product, Category, Subcategory, Brand, ProductVariant


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductVariantSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
