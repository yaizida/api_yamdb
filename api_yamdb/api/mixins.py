from reviews.validators import (validate_non_reserved)


class UsernameValidationMixin():
    def validate_username(self, value):
        value = validate_non_reserved(value)
        return value
