from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import AdminOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from django.db import IntegrityError
from rest_framework.validators import ValidationError

from reviews.models import User
from .serializers import (UserSerializer, GetAuthTokenSerializer,
                          SignUpSerializer, UserProfileSerializer)
from .registration.send_email import send_email
from .registration.token_generator import get_token_for_user

ERROR_SIGNUP_USERNAME_OR__MAIL = (
    'Пользователь с таким email или username уже существует'
)


class CreateUserView(CreateAPIView):
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
            raise ValidationError(ERROR_SIGNUP_USERNAME_OR__MAIL)
        confirmation_code = default_token_generator.make_token(user)
        print(confirmation_code)
        user.confirmation_code = confirmation_code
        user.save()
        send_email(user.email, user.confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAuthTokenView(APIView):
    """CBV для получения и обновления токена."""

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {"confirmation_code": ["Неверный код подтверждения"]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(get_token_for_user(user), status=status.HTTP_200_OK)


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
        serializer = UserProfileSerializer(
            request.user, partial=True, data=request.data
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "PATCH":
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
