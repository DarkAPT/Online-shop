from django import template

from products.models import Products,CharacteristicsSet

register = template.Library()

@register.simple_tag()
def tag_products():
    return Products.objects.all()

@register.simple_tag()
def tag_characteristics_sets():
    return CharacteristicsSet.objects.all()
