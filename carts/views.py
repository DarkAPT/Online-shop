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

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

    carts = get_user_carts(request)

    return JsonResponse({'cart_count': carts.count()})


def cart_change(request):
    url_data = request.POST.get("url_data")
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_cart = get_user_carts(request)
    if url_data == "create_order":
        carts_items_html = render_to_string("orders/async/create_order.html", {"carts": user_cart}, request=request)
    else:
        carts_items_html = render_to_string("users/async/cart_order.html", {"carts": user_cart}, request=request)

    response_data={
        "carts_items_html": carts_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    url_data = request.POST.get("url_data")
    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity

    cart.delete()
    user_cart = get_user_carts(request)
    if url_data == "create_order":
        carts_items_html = render_to_string("orders/async/create_order.html", {"carts": user_cart}, request=request)
    else:
        carts_items_html = render_to_string("users/async/cart.html", {"carts": user_cart}, request=request)

    response_data={
        "carts_items_html": carts_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
