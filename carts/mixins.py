from django.template.loader import render_to_string
from carts.models import Cart
from carts.utils import get_user_carts


class CartMixin:
    def get_user_cart(self, request, product=None, cart_id=None):
        if request.user.is_authenticated:
            kwargs_query = {"user": request.user}
        else:
            kwargs_query = {"session_key": request.session.session_key}

        if product:
            kwargs_query["product"] = product
        if cart_id:
            kwargs_query["id"] = cart_id

        return Cart.objects.filter(**kwargs_query).first()

    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}
        url_data = request.POST.get("url_data")

        if url_data == "create_order":
            return render_to_string("orders/async/create_order.html", context, request=request)
        return render_to_string("users/async/cart.html", context, request=request)
