from django.http import JsonResponse
from django.template.loader import render_to_string
from carts.models import Cart, Favourites
from carts.utils import get_user_carts, get_user_favourites, product_in_cart_util
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
    prod_in_cart = product_in_cart_util(request, product_id).get()
    prod_quant = render_to_string("products/async/product_quantity.html", {"cart":prod_in_cart}, request=request)

    response_data={
        'cart_count': carts.count(),
        "prod_quant": prod_quant,
    }

    return JsonResponse(response_data)


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


def favourites_add_remove(request):
    product_id = request.POST.get("product_id")
    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        favourite = Favourites.objects.filter(user=request.user, product=product)

        if favourite.exists():
            favourite.delete()
        else:
            Favourites.objects.create(user=request.user, product=product)
    else:
        favourite = Favourites.objects.filter(session_key=request.session.session_key, product=product)

        if favourite.exists():
            favourite.delete()
        else:
            Favourites.objects.create(session_key=request.session.session_key, product=product)

    user_favourites = get_user_favourites(request)
    favourites_items = render_to_string("users/async/favourites.html", {"favourites":user_favourites}, request=request)
    response_data = {
        "favourites_items": favourites_items,
        "favourites_count": user_favourites.count()
    }
    return JsonResponse(response_data)
