from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"
ERROR_WRONG_YEAR = ("Год должен быть указан в диапозоне от "
                    "1 до текущего года: {current_year}")


def validate_non_reserved(value):
    """Запрещает использовать 'me в качестве username'"""
    if value in settings.RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value


def validate_year(value):
    current_year = timezone.now().year
    if not (0 < value <= current_year):
        raise ValidationError(
            ERROR_WRONG_YEAR.format(current_year=current_year)
        )
