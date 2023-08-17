from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Product, Category, Subcategory, Brand, ProductVariant
from .serializers import ProductSerializer, CategorySerializer, SubcategorySerializer, BrandSerializer, ProductVariantSerializer


class ProductListAPIView(ListAPIView):
    """List all products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    """Retrieve a product"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryListAPIView(ListAPIView):
    """List all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryListAPIView(ListAPIView):
    """List all subcategories"""
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class BrandListAPIView(ListAPIView):
    """List all brands"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductsByCategoryAPIView(ListAPIView):
    """List all products by category"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)


class ProductsBySubcategoryAPIView(ListAPIView):
    """List all products by subcategory"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['subcategory_id']
        return Product.objects.filter(subcategory_id=subcategory_id)


class ProductsByBrandAPIView(ListAPIView):
    """List all products by brand"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        return Product.objects.filter(brand_id=brand_id)
