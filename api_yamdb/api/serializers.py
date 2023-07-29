from rest_framework.serializers import (ModelSerializer, )

from .mixins import UsernameValidationMixin
from rest_framework.serializers import (CharField, EmailField, Serializer)
from reviews.models import User


class SignupSerializer(Serializer, UsernameValidationMixin):
    username = CharField(
        required=True,
        max_length=150,
    )
    email = EmailField(
        required=True,
        max_length=150,
    )


class UserSerializer(ModelSerializer, UsernameValidationMixin):
    class Meta:
        model = User
        fields = ('__all__')
