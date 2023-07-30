from django.core.exceptions import ValidationError


USERNAME_INVALID_PATTERN = compile(r'[^\w.@+-]+')
RESERVED_USERNAMES = ('me',)

ERROR_USERNAME_RESERVED = ("'{value}' нельзя использовать в качестве "
                           "имени пользователя")
ERROR_USERNAME_SYMBOL = "Нельзя использовать символы '{}' в username"


def validate_non_reserved(value):
    """Запрещает использовать 'me в качестве username'"""
    if value in RESERVED_USERNAMES:
        raise ValidationError(ERROR_USERNAME_RESERVED.format(value=value))
    return value


def validate_username_allowed_chars(value):
    """Запрещает использовать в поле username запрещенные символы"""
    invalid_chars = USERNAME_INVALID_PATTERN.findall(value)
    if invalid_chars:
        raise ValidationError(
            ERROR_USERNAME_SYMBOL.format(''.join(set(''.join(invalid_chars))))
        )
    return value
