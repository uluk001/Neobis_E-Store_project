from django.urls import path, include
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    CategoryListAPIView,
    SubcategoryListAPIView,
    BrandListAPIView,
    ProductsByCategoryAPIView,
    ProductsBySubcategoryAPIView,
    ProductsByBrandAPIView,
    CreateProductReviewView,
    ProductReviewListView,
)

urlpatterns = [
    path('list/', ProductListAPIView.as_view()), # /api/v1/products/list/
    path('<int:pk>/', ProductDetailAPIView.as_view()), # /api/v1/products/1/
    path('categories/', CategoryListAPIView.as_view()), # /api/v1/products/categories/
    path('subcategories/', SubcategoryListAPIView.as_view()), # /api/v1/products/subcategories/
    path('brands/', BrandListAPIView.as_view()), # /api/v1/products/brands/
    path('category/<int:category_id>/', ProductsByCategoryAPIView.as_view()), # /api/v1/products/category/1/
    path('subcategory/<int:subcategory_id>/', ProductsBySubcategoryAPIView.as_view()),  # /api/v1/products/subcategory/1/
    path('brand//', ProductsByBrandAPIView.as_view()), # /api/v1/products/brand/1/
    path('review/create/', CreateProductReviewView.as_view()), # /api/v1/products/review/create/
    path('review/list/<int:product_id>', ProductReviewListView.as_view()), # /api/v1/products/review/list/1/
]