from rest_framework import generics, status
from rest_framework.response import Response
from apps.carts.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

def create_order_for_user(user):
    cart = Cart.objects.get(user=user)
    total_price = sum([item.product_variant.product.price * item.quantity for item in cart.items.all()])

    # Create an order
    order = Order.objects.create(user=user, total_price=total_price, status='Pending')
    
    # Create order items based on cart items
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_variant=cart_item.product_variant,
            quantity=cart_item.quantity,
            price=cart_item.product_variant.product.price * cart_item.quantity
        )
    
    # Clear the cart
    cart.items.all().delete()
    
    return order

class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        order = create_order_for_user(user)
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
