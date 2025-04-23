from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from orders.models import Order


@shared_task()
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} payment Confirmation'
    message = f'Здравствуйте, {order.user.username}. Ваш заказ был успешно оформлен.\n\n'
    user_email = order.user.email

    mail = send_mail(subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user_email])
    return mail
