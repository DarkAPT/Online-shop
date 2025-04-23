from django import template

from products.models import Products,CharacteristicsSet,Categories,PropertyValues, Review

register = template.Library()

@register.simple_tag()
def tag_products():
    return Products.objects.all()

@register.simple_tag()
def tag_characteristics_sets(product_id):
    return CharacteristicsSet.objects.filter(productid_id=product_id)\
    .select_related('propertyvalueid', "propertyid")\
    .values('propertyvalueid__value', "propertyid__name")

@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

@register.simple_tag()
def tag_property_values(property_name):
    return PropertyValues.objects.filter(propertyid__name=property_name).order_by('order_value')

@register.simple_tag()
def get_comments(product_id):
    return Review.objects.filter(product__id=product_id).exclude(message__in=[None, ''])

@register.simple_tag()
def get_review(request,product_id):
    review = Review.objects.filter(user__id=request.user.id).filter(product__id=product_id)
    if review:
        return review[0]
    return None
