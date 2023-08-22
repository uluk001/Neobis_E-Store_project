from django.urls import path

from .views import AddToCartView, CartItemsView, RemoveCartItemView

urlpatterns = [
    path('add/', AddToCartView.as_view()),  # api/v1/carts/add/
    path('items/', CartItemsView.as_view()),  # api/v1/carts/items/
    path('remove/', RemoveCartItemView.as_view()),  # api/v1/carts/remove/
]
