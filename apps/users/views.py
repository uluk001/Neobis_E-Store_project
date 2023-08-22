from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Address
from .serializers import AddressSerializer
from rest_framework.permissions import IsAuthenticated


class CreateAddressView(generics.CreateAPIView):
    """
    Create address for user
    
    Use this endpoint to create address for user

    Parameters:
    address - address for user
    city - city for user
    country - country for user
    postal_code - postal code for user
    is_default - is default address for user
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        address = request.data.get('address')
        city = request.data.get('city')
        country = request.data.get('country')
        postal_code = request.data.get('postal_code')
        is_default = bool(request.data.get('is_default'))
        address_obj = Address.objects.create(user=user, address=address, city=city, country=country, postal_code=postal_code, is_default=is_default)

        serializer = self.get_serializer(address_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)