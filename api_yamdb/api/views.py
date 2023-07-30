from datetime import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import AdminOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes

from reviews.models import User
from .serializers import UserSerializer, GetAuthTokenSerializer
from .registration.send_email import send_email
from .registration.token_generator import get_token_for_user

ERROR_SIGNUP_USERNAME_OR__MAIL = (
    'Пользователь с таким email или username уже существует'
)


class UserViewSet(ModelViewSet):
    filter_backends = (SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request, pk=None):
        if request.method == "GET":
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data)
        if request.method == "PATCH":
            user = get_object_or_404(User, username=self.request.user)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    email = request.data["email"]
    username = email.split("@")[0]
    user = User.objects.create(
        username=username,
        email=email,
        last_login=datetime.now(),
    )
    confirmation_code = default_token_generator.make_token(user)
    send_email(email, confirmation_code)
    return Response(confirmation_code, status=status.HTTP_200_OK)


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


class UserMeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            UserSerializer(instance=request.user).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = UserSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=serializer.instance.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
