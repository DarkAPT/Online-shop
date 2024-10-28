from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts
from products.models import Products

def cart_add(request):
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    carts = get_user_carts(request)

    return JsonResponse({'cart_count': carts.count()})


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_cart = get_user_carts(request)
    carts_items_html = render_to_string("users/async/cart_order.html", {"carts": user_cart}, request=request)

    response_data={
        "carts_items_html": carts_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity

    cart.delete()
    user_cart = get_user_carts(request)
    carts_items_html = render_to_string("users/async/cart.html", {"carts": user_cart}, request=request)

    response_data={
        "carts_items_html": carts_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
