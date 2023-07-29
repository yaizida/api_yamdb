import random
import string
from os import getenv

from django.core.mail import send_mail

from dotenv import load_dotenv

load_dotenv()


CONFIRMATION_CODE_LENGTH = 10
DEFAULT_SUBJECT = 'Код подтверждения от Yamdb'
DEFAULT_MESSAGE = 'Ваш код подтверждения - {}'
DEFAULT_FROM_EMAIL = getenv('EMAIL_HOST_USER')


def get_code():
    return ''.join(
        random.choices(
            population=string.digits,
            k=CONFIRMATION_CODE_LENGTH,
        )
    )


def send_email(user_email, code):
    send_mail(
        subject=DEFAULT_SUBJECT,
        message=DEFAULT_MESSAGE.format(code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
    )
