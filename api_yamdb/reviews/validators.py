from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator


ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"


def validate_non_reserved(value):
    """Запрещает использовать 'me в качестве username'"""
    if value in settings.RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value


unicode_username_validator = UnicodeUsernameValidator


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0
