from carts.models import Cart, Favourites


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).order_by('product__id').select_related('product')

    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).order_by('product__id').select_related('product')


def product_in_cart_util(request, product_id):
    if request.user.is_authenticated:
        temp = Cart.objects.filter(user=request.user).filter(product__id=product_id)
        if temp.exists():
            return temp
        return False
    if Cart.objects.filter(session_key=request.session.session_key).filter(product__id=product_id).exists():
        return Cart.objects.filter(session_key=request.session.session_key).filter(product__id=product_id)
    return False


def get_user_favourites(request):
    if request.user.is_authenticated:
        return Favourites.objects.filter(user=request.user).order_by('product__id').select_related('product')
    if not request.session.session_key:
        request.session.create()
    return Favourites.objects.filter(session_key=request.session.session_key).order_by('product__id').select_related('product')



def product_in_favourites_util(request, product_id):
    if request.user.is_authenticated:
        temp = Favourites.objects.filter(user=request.user).filter(product__id=product_id)
        if temp.exists():
            return temp
        return False
    if Favourites.objects.filter(session_key=request.session.session_key).filter(product__id=product_id).exists():
        return Favourites.objects.filter(session_key=request.session.session_key).filter(product__id=product_id)
    return False
