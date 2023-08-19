from django.contrib import admin
from .models import Category, Subcategory, Brand, Product, ProductVariant, Review

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory', 'brand')
    list_filter = ('category', 'subcategory', 'brand')
    search_fields = ('name', 'description')

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('product', 'user')
    search_fields = ('product', 'user')

admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Review, ReviewAdmin)
