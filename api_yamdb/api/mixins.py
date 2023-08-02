from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from reviews.validators import (validate_non_reserved,
                                validate_username_allowed_chars)


class CategoryGenreMixinSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class UsernameValidationMixin:
    def validate_username(self, value):
        value = validate_non_reserved(value)
        validate_username_allowed_chars(value)
        return value
