from rest_framework import serializers
from reviews.models import Category, Genre, Title, Review, Comment, User
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    "Сериализатор для GET запроса"
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleEditSerializer(serializers.ModelSerializer):
    "Сериализатор для ввода, изменения и удаления данных"
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']

    def validate_score(self, value):
        """Проверка оценки"""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Оценка должна быть в диапазоне от 1 до 10"
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
