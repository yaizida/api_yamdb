from rest_framework import routers

from django.urls import path, include

from .views import UserViewSet

app_name = 'api'

VERSION_1 = 'v1/'
router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path(VERSION_1, include(routers.urls))
]
