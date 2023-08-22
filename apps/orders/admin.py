from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email')

    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
