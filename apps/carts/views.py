from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Cart, CartItem
from .permissions import IsOwner
from .serializers import AddToCartSerializer, CartItemSerializer

class AddToCartView(CreateAPIView):
    """
    Add product to cart

    Use this endpoint to add a product to cart.

    Parameters:
    - `product_id` (int): ID of the product to add.
    - `quantity` (int): Quantity of the product to add.
    """
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.request.user
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise ValidationError({"message": "Товар с данным ID не найден."}, code=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=user)
        
        try:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
        except CartItem.MultipleObjectsReturned:
            raise ValidationError({"message": "Ошибка при добавлении товара в корзину."}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        response_message = f"{product.name} добавлена в корзину ({cart_item.quantity})"
        
        return Response({"message": response_message})



class CartItemDeleteView(CreateAPIView):
    """
    Delete product from cart

    Use this endpoint to delete a product from cart.

    Parameters:
    - `product_id` (int): ID of the product to delete.
    """
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data['product_id']

        cart_item = CartItem.objects.get(cart__user=user, product_id=product_id)
        cart_item.delete()

        response_message = f"Товар удален из корзины"
        
        return Response({"message": response_message})


class CartListView(ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def get_total_price(self, queryset):
        total_price = sum(item.product.price * item.quantity for item in queryset)
        return total_price

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total_price = self.get_total_price(queryset)
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'cart_items': serializer.data,
            'total_price': total_price
        }
        return Response(response_data)


class CartItemUpdateView(CreateAPIView):
    """
    Update product quantity in cart

    Use this endpoint to update product quantity in cart.

    Parameters:
    - `product_id` (int): ID of the product to update.
    - `quantity` (int): New quantity of the product.
    """
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        product_id = request.data['product_id']
        quantity = request.data['quantity']

        cart_item = CartItem.objects.get(cart__user=user, product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()

        response_message = f"Количество товара обновлено"
        
        return Response({"message": response_message})
