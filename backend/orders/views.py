import uuid
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from yookassa import Configuration, Payment

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.tasks import send_order_confirmation_email

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = "orders/create_order.html"
    form_class = CreateOrderForm
    success_url = reverse_lazy("user:profile")

    def get_initial(self):
        initial = super().get_initial()
        initial["first_name"] = self.request.user.first_name
        initial["last_name"] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )
                    for item in cart_items:
                        product = item.product
                        name = item.product.name
                        price=item.product.sell_price_for_carts()
                        quantity=item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество товара {name} на складе\
                                                       В наличии - {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()


                    idempotence_key = uuid.uuid4()
                    currency = 'RUB'
                    description = 'Заказ на сайте'
                    payment = Payment.create({
                        "amount": {
                            "value": str(cart_items.total_price(is_int=True)),
                            "currency": currency
                        },
                        "confirmation": {
                            "type": "redirect",
                            "return_url": self.request.build_absolute_uri(reverse('orders:payment_success')),
                        },
                        "description": description,
                        "capture": True,
                        "test": True,
                    }, idempotence_key)

                    confirmation_url = payment.confirmation.confirmation_url
                    return redirect(confirmation_url)
        except ValidationError as e:
            messages.success(self.request, str(e))
            return redirect('orders:create_order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Оформление заказа"
        return context


class PaymentSuccessView(TemplateView):
    template_name = 'users/profile.html'
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        cart_items.delete()
        order_id = Order.objects.all().filter(user=user).order_by("-id").first().id
        send_order_confirmation_email.delay(order_id)
        messages.success(request, "Payment Success")
        return redirect("user:profile")

class PaymentFailedView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        messages.error(request, "Payment Failed")
        return redirect("orders:crete_order")
    