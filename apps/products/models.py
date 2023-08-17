from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Model definition for Category."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    """Model definition for Subcategory."""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    """Model definition for Brand."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Model definition for Product."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk})

class ProductVariant(models.Model):
    """Model definition for ProductVariant."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"
