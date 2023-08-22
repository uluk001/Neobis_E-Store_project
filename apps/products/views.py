from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Product, Category, Subcategory, Brand, ProductVariant, Review
from .serializers import ProductSerializer, CategorySerializer, SubcategorySerializer, BrandSerializer, ProductVariantSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .filters import ProductFilter
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated


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
    """
    Product details.

    Use this endpoint to get details of a product.

    Parameters:
    - `product_id` (int): ID of the product to get details.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class CategoryListAPIView(ListAPIView):
    """
    List of categories.

    Use this endpoint to get a list of all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryListAPIView(ListAPIView):
    """
    List of subcategories.

    Use this endpoint to get a list of all subcategories.
    """
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class BrandListAPIView(ListAPIView):
    """
    List of brands.

    Use this endpoint to get a list of all brands.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductsByCategoryAPIView(ListAPIView):
    """
    List of products by category.

    Use this endpoint to get a list of all products by category.

    Parameters:
    - `category_id` (int): ID of the category to get products.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)


class ProductsBySubcategoryAPIView(ListAPIView):
    """
    List of products by subcategory.

    Use this endpoint to get a list of all products by subcategory.

    Parameters:
    - `subcategory_id` (int): ID of the subcategory to get products.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        subcategory_id = self.kwargs['subcategory_id']
        return Product.objects.filter(subcategory_id=subcategory_id)


class ProductsByBrandAPIView(ListAPIView):
    """
    List of products by brand.

    Use this endpoint to get a list of all products by brand.

    Parameters:
    - `brand_id` (int): ID of the brand to get products.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        brand_id = self.kwargs['brand_id']
        return Product.objects.filter(brand_id=brand_id)


class CreateProductReviewView(CreateAPIView):
    """
    Create a review for a product.

    Use this endpoint to create a review for a product.

    Parameters:
    - `product_id` (int): ID of the product to create a review.
    - `rating` (int): Rating of the product. Must be between 1 and 5.
    - `comment` (str): Comment for the product.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        product_id = request.data['product_id']
        rating = request.data['rating']
        comment = request.data['comment']
        user = self.request.user

        review = Review.objects.create(
            product_id=product_id,
            user=user,
            rating=rating,
            comment=comment
        )

        reviews = Review.objects.filter(product_id=product_id)
        total_ratings = len(reviews)
        total_sum = sum(int(review.rating) for review in reviews)
        average_rating = total_sum / total_ratings

        product = Product.objects.get(id=product_id)
        product.average_rating = average_rating
        product.total_ratings = total_ratings
        product.save()

        response_message = f"Ваш отзыв успешно добавлен"

        return Response({"message": response_message})


class ProductReviewListView(ListAPIView):
    """
    List of reviews for a product.

    Use this endpoint to get a list of all reviews for a product.

    Parameters:
    - `product_id` (int): ID of the product to get reviews.
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)
