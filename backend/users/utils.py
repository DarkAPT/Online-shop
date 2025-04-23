from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from celery import shared_task

from users.models import User
from .tokens import account_activation_token

@shared_task()
def activate_email(user_id, to_email, domain, protocol):
    user = User.objects.get(pk=user_id)
    mail_subject = "Подтверждение аккаунта"
    message = render_to_string("users/activate_account.html", {
        "user": user,
        "domain": domain,
        "uid": urlsafe_base64_encode(force_bytes(user)),
        "token": account_activation_token.make_token(user),
        "protocol": protocol
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()
