from django.core.mail import send_mail
from django.conf import settings


CONFIRMATION_CODE_LENGTH = 10
DEFAULT_SUBJECT = 'Код подтверждения от Yamdb'
DEFAULT_MESSAGE = 'Ваш код подтверждения - {}'
DEFAULT_FROM_EMAIL = settings.ADMIN_EMAIL


def send_email(user_email, code):
    send_mail(
        subject=DEFAULT_SUBJECT,
        message=DEFAULT_MESSAGE.format(code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
    )
