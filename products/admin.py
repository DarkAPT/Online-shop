from django.contrib import admin

from products.models import Categories,Products,Properties,PropertyValues,CharacteristicsSet

admin.site.register(Properties)
admin.site.register(PropertyValues)
admin.site.register(CharacteristicsSet)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
