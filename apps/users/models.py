from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""
    pass


class Address(models.Model):
    """Address model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
