from django.contrib import admin
from .models import Order, OrderItem
from .models import Order, OrderItem, ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'order']
    list_editable = ['price', 'order']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'paid', 'created', 'order_total'
    ]
    
    list_filter = ['paid', 'created'] 
    
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'address']
    readonly_fields = ['payment_id', 'created']

    def order_total(self, obj):
        return f"{obj.get_total_cost()} BYN"
    order_total.short_description = 'Сумма заказа'