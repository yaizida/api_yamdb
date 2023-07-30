from rest_framework import serializers

from reviews.models import User
from reviews.validators import (validate_non_reserved,)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserProfileSerializer(UserSerializer):
    """Сериализатор модели User для профиля пользователя."""
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        max_length=150,
        required=False,
        validators=[validate_non_reserved, ],
    )
    email = serializers.EmailField(
        max_length=150,
        required=False,
    )

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""

        if not User.objects.filter(
            username=data.get("username"), email=data.get("email")
        ).exists():
            if User.objects.filter(username=data.get("username")):
                raise serializers.ValidationError(
                    "Пользователь с таким username уже существует"
                )

            if User.objects.filter(email=data.get("email")):
                raise serializers.ValidationError(
                    "Пользователь с таким Email уже существует"
                )

        return data


class GetAuthTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_non_reserved, ],
    )
    confirmation_code = serializers.CharField(
        required=True, max_length=150,
    )
