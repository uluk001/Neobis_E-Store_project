from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import IsOwner
from .serializers import AddToCartSerializer, CartItemSerializer
from .models import CartItem, Cart
from apps.products.models import ProductVariant


class AddToCartView(CreateAPIView):
    """
    Add product to cart
    
    Use this endpoint to add a product to cart.

    Parameters:
    - `product_variant_id` (int): ID of the product variant to add to cart.
    - `quantity` (int): Quantity of the product to add to cart.
    """
    serializer_class = AddToCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_variant_id']
        quantity = serializer.validated_data['quantity']
        user = self.request.user
        product_variant = ProductVariant.objects.get(id=product_id)
        
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)


class CartItemsView(ListAPIView):
    """
    List of cart items.

    Use this endpoint to get a list of all cart items.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)


class RemoveCartItemView(CreateAPIView):
    """
    Remove product from cart.

    Use this endpoint to remove a product from cart.

    Parameters:
    - `product_variant_id` (int): ID of the product variant to remove from cart.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        product_variant_id = request.data.get('product_variant_id')
        user = self.request.user
        product_variant = ProductVariant.objects.get(id=product_variant_id)
        try:
            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.get(cart=cart, product_variant=product_variant)
            cart_item.delete()
            return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)
