from django.urls import path

from .views import CreateOrderView, MyOrdersView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='order-create'),  # /api/v1/orders/create/
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),  # /api/v1/orders/my-orders/
]
