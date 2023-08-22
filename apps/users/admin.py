from django.contrib import admin

from .models import Address, User


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

    inlines = [AddressInline]


admin.site.register(User, UserAdmin)
