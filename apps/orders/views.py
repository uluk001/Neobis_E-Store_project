from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response

from apps.carts.models import Cart

from .models import Order, OrderItem
from .serializers import OrderSerializer


def check_user_address(request):
    user = request.user

    addresses = user.address_set.all()

    if not addresses.exists() or not addresses.filter(is_default=True).exists():
        return redirect('')
    else:
        return None


def create_order_for_user(user):
    cart = Cart.objects.get(user=user)
    total_price = sum([item.product_variant.product.price * item.quantity for item in cart.items.all()])

    if total_price > 20000:
        discount = total_price * 0.1
        total_price -= discount

    order = Order.objects.create(user=user, total_price=total_price, status='Pending')

    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_variant=cart_item.product_variant,
            quantity=cart_item.quantity,
            price=cart_item.product_variant.product.price * cart_item.quantity
        )

    cart.items.all().delete()

    return order


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


def create(self, request, *args, **kwargs):
    user = self.request.user

    if user.cart.cart_items.count() == 0:
        return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    order = create_order_for_user(user)

    serializer = self.get_serializer(order)
    if check_user_address(request):
        return Response({'error': 'You must have at least one address'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyOrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return user.order_set.all()
