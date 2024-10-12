from django import template

from products.models import Products,CharacteristicsSet,Categories,PropertyValues

register = template.Library()

@register.simple_tag()
def tag_products():
    return Products.objects.all()

@register.simple_tag()
def tag_characteristics_sets():
    return CharacteristicsSet.objects.all()

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag()
def tag_property_values():
    return PropertyValues.objects.all().order_by('order_value')
