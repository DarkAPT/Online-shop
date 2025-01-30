from django.contrib import admin

from carts.models import Cart, Favourites


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'created_date'
    search_fields = 'product', 'quantity', 'created_date'
    readonly_fields = ('created_date',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "created_date",]
    list_filter = ["user", "product__name"]

admin.site.register(Favourites)
