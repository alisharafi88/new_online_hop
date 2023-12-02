from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'updated_on', 'is_paid']
    list_filter = ['is_paid', 'updated_on']
    inlines = [OrderItemInline,]
    search_fields = ['user', 'updated_on']
    list_select_related = ['user']


admin.site.register(OrderItem)
