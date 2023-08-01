from django.core.exceptions import ValidationError

RESERVED_USERNAMES = ('me',)

ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"


def validate_non_reserved(value):
    """Запрещает использовать 'me в качестве username'"""
    if value in RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value
