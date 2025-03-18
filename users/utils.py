from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token


def activate_email(request, user, to_email):
    mail_subject = "Подтверждение аккаунта"
    message = render_to_string("users/activate_account.html", {
        "user": user,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "protocol": "https" if request.is_secure() else "http"
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Проверьте почту {to_email}, чтобы подтвердить аккаунт")
    else:
        messages.error(request, f"Не удалось отправить сообщение на почту: {to_email}")
