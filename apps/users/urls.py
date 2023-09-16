from django.urls import path


from .views import CreateAddressView, ProfileView

urlpatterns = [
    path('create_address/', CreateAddressView.as_view(), name='address-create'),  # /api/v1/users/create_address/
    path('profile/', ProfileView.as_view(), name='profile'),  # /api/v1/users/profile/
]
