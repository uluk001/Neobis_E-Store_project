from django.urls import path
from .views import CreateAddressView

urlpatterns = [
    path('create_address/', CreateAddressView.as_view(), name='address-create'), # /api/v1/users/create_address/
]