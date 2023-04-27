from random import randint
from django.core.mail import send_mail

from yanki.settings import SITE_NAME


def send_activate_email_message(email):
    subject = f'Активация аккаунта на сайте {SITE_NAME}'
    cod = randint(1000, 9999)
    message = f"Ваш код подтверждения: {cod}"
    send_mail(subject, message, "Privet!", [email, ])
    return cod
