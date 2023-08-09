from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from django.db import IntegrityError
from rest_framework.validators import ValidationError
from rest_framework import viewsets, response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import mixins

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .serializers import (UserSerializer, GetAuthTokenSerializer,
                          SignUpSerializer)
from .permissions import (
    IsAuthorOrAdminOrModerator,
    AdminOnly,
    IsAdminOrReadOnly
)
from reviews.models import User
from .registration.send_email import send_email
from .filters import TitleFilter


ERROR_SIGNUP_USERNAME_OR_MAIL = (
    'Пользователь с таким email или username уже существует'
)


class CreateUserView(CreateAPIView):
    """Вьюсет для создания пользователя"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            raise ValidationError(ERROR_SIGNUP_USERNAME_OR_MAIL)
        confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_email(user.email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAuthTokenView(APIView):
    """CBV для получения и обновления токена."""

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return response.Response(
                {'token': str(token)}, status=status.HTTP_200_OK
            )
        return response.Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    """Вьюсет модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ("get", "post", "delete", "patch")

    @action(
        detail=False,
        methods=("get", "patch"),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        serializer = UserSerializer(
            request.user, partial=True, data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "PATCH":
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый класс для обработки разрешений."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [
                IsAuthenticatedOrReadOnly,
                IsAuthorOrAdminOrModerator
            ]
        return super().get_permissions()


class BaseCategoryGenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(BaseCategoryGenreViewSet):
    """ViewSet для категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class GenreViewSet(BaseCategoryGenreViewSet):
    """ViewSet для жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(BaseViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_title_id(self):
        return self.kwargs.get('title_id')

    def get_queryset(self):
        return Review.objects.filter(title_id=self.get_title_id())

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.get_title_id())

        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            raise ValidationError("Вы уже оставляли отзыв на это произведение")

        serializer.save(author=self.request.user, title=title)


class CommentViewSet(BaseViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_review_id(self):
        return self.kwargs.get('review_id')

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.get_review_id())

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.get_review_id())
        serializer.save(author=self.request.user, review=review)


def __init__(self, you='Ты', who='Лох'):
    self.you = you
    self.who = who
