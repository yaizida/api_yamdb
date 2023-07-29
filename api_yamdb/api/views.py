from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import AdminOnly
from rest_framework import status
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from reviews.models import User
from .serializers import SignupSerializer, UserSerializer
from .auth import get_code, send_email

ERROR_SIGNUP_USERNAME_OR__MAIL = (
    'Пользователь с таким email или username уже существует'
)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email')
            )
        except IntegrityError:
            raise ValidationError(ERROR_SIGNUP_USERNAME_OR__MAIL)
        user.confirmation_code = get_code()
        user.save()
        send_email(user.email, user.confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    filter_backends = (SearchFilter,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly]
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


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


class TokenAPIView(APIView):
    permission_classes = [AllowAny]
    pass
