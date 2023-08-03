from django.core.exceptions import ValidationError
from re import compile

RESERVED_USERNAMES = ('me',)

ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"
USERNAME_INVALID_PATTERN = compile(r'[^\w.@+-]+')


def validate_non_reserved(value):
    """Запрещает использовать 'me в качестве username'"""
    if value in RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value


def validate_username_allowed_chars(value):
    """Запрещает использовать символы из перечня запрещенных символов"""
    invalid_chars = USERNAME_INVALID_PATTERN.findall(value)
    if invalid_chars:
        raise ValidationError(
            ERROR_USERNAME_SYMBOL.format(''.join(set(''.join(invalid_chars))))
        )
    return value
