from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Address
from .serializers import AddressSerializer


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


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve profile for user

    Use this endpoint to retrieve profile for user

    Parameters:
    username - username for user
    first_name - first name for user
    last_name - last name for user
    email - email for user
    address - address for user
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        user.username = request.data.get('username')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        user.email = request.data.get('email')
        user.address = request.data.get('address')
        user.save()

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
