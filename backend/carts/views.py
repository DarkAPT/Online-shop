from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from carts.mixins import CartMixin
from carts.models import Cart, Favourites
from carts.utils import get_user_carts, get_user_favourites, product_in_cart_util, product_in_favourites_util
from products.models import Products

class CartAddView(CartMixin,View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)

        cart = self.get_user_cart(request, product=product)
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key = request.session.session_key if not request.user.is_authenticated else None,
                                product=product, quantity=1)

        carts = get_user_carts(request)
        prod_in_cart = product_in_cart_util(request, product_id).get()
        prod_quant = render_to_string("products/async/product_quantity.html", {"cart":prod_in_cart}, request=request)

        response_data={
            'cart_count': carts.count(),
            "prod_quant": prod_quant,
        }

        return JsonResponse(response_data)

class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")

        cart = self.get_user_cart(request, cart_id = cart_id)

        cart.quantity = quantity
        cart.save()

        response_data={
            "carts_items_html": self.render_cart(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)

class CartRemoveView(CartMixin,View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = Cart.objects.get(id=cart_id)
        quantity = cart.quantity

        cart.delete()

        response_data={
            "carts_items_html": self.render_cart(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)

class FavouritesView(View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)

        favourite = product_in_favourites_util(request, product_id)
        if favourite:
            favourite.delete()
        else:
            Favourites.objects.create(user=request.user if request.user.is_authenticated else None,
                                      session_key=request.session.session_key if not request.user.is_authenticated else None,
                                      product=product
            )

        user_favourites = get_user_favourites(request)
        favourites_items = render_to_string("users/async/favourites.html", {"favourites":user_favourites}, request=request)
        response_data = {
            "favourites_items": favourites_items,
            "favourites_count": user_favourites.count()
        }
        return JsonResponse(response_data)
