from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "price", "quantity")
    search_fields = ("order", "name")

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "status",
        "payment_on_get",
        "is_paid",
        "create_data",
    )

    search_fields = (
        "payment_on_get",
        "is_paid",
        "create_data",
    )
    readonly_fields = ("create_data",)
    extra = 0

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "name", "price", "quantity"
    search_field = ("name",)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        "payment_on_get",
        "is_paid",
        "create_data"
    )

    search_fields = (
        'id',
    )
    readonly_fields = ("create_data",)
    list_filter = (
        "is_paid",
        'status',
        "payment_on_get",
    )
    inlines = (OrderItemTabulareAdmin,)
