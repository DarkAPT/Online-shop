from django import template
from carts.utils import get_user_carts, get_user_favourites, product_in_cart_util, product_in_favourites_util

register = template.Library()

@register.simple_tag()
def user_carts(request):
    return get_user_carts(request)


@register.simple_tag()
def product_in_cart(request, product_id):
    return product_in_cart_util(request, product_id)


@register.simple_tag()
def user_favourites(request):
    return get_user_favourites(request)

@register.simple_tag()
def product_in_favourites(request, product_id):
    return product_in_favourites_util(request, product_id)
