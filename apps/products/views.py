from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Product, Category, Subcategory, Brand, ProductVariant
from .serializers import ProductSerializer, CategorySerializer, SubcategorySerializer, BrandSerializer, ProductVariantSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import OrderingFilter



class ProductListAPIView(ListAPIView):
    """
    List of products with optional filtering and sorting.

    Use query parameters to filter and sort the list of products.

    Parameters:
    - `category` (int): Filter products by category ID.
    - `brand` (int): Filter products by brand ID.
    - `min_price` (decimal): Minimum price for filtering.
    - `max_price` (decimal): Maximum price for filtering.
    - `ordering` (str): Sort products by specified field. Examples: `price`, `name`.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['price', 'name']


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
