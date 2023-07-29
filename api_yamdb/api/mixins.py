from reviews.validators import (validate_non_reserved,
                                validate_username_allowed_chars)


class UsernameValidationMixin:
    def validate_username(self, value):
        value = validate_non_reserved(value)
        validate_username_allowed_chars(value)
        return value
