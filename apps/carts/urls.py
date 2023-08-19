from .views import AddToCartView, CartListView, CartItemDeleteView, CartItemUpdateView
from django.urls import path

urlpatterns = [
    path('add/', AddToCartView.as_view()), # /api/v1/carts/add/
    path('list/', CartListView.as_view()), # /api/v1/carts/list/
    path('delete/', CartItemDeleteView.as_view()), # /api/v1/carts/delete/
    path('update/', CartItemUpdateView.as_view()), # /api/v1/carts/update/
]