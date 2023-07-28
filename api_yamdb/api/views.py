# from django.shortcuts import get_object_or_404
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets

from reviews.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
