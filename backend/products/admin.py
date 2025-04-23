from django.contrib import admin

from products.models import Categories,Products,Properties,PropertyValues,CharacteristicsSet, Review

admin.site.register(Properties)
admin.site.register(PropertyValues)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'product_id', 'message', 'mark', 'is_anonymous', 'create_data']

class CharacteristicsSetTabAdmin(admin.TabularInline):
    model = CharacteristicsSet
    fields = ("propertyvalueid","propertyid")
    search_fields = ("propertyvalueid",)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    list_display = ['name', 'quantity', 'price','discount']
    list_editable = ['price','discount']
    search_fields = ['name']
    inlines = [CharacteristicsSetTabAdmin,]

@admin.register(CharacteristicsSet)
class CharacteristicsSetAdmin(admin.ModelAdmin):
    list_display = ['productid', 'propertyvalueid']
    list_filter = ['propertyvalueid']

    @admin.display()
    def get_all_sets(self, obj):
        property_values = CharacteristicsSet.objects.filter(productid=obj.productid).select_related('propertyvalueid').values_list('propertyvalueid__value', flat=True)
        return ', '.join(list(property_values))
