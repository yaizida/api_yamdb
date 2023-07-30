from rest_framework import routers

from django.urls import path, include

from .views import (CreateUserView, UserViewSet,
                    GetAuthTokenView)

app_name = 'api'

VERSION_1 = 'v1/'

auth_urls = [
    path('auth/signup/', CreateUserView.as_view(), name='signup'),
    path('auth/token/', GetAuthTokenView.as_view(), name='token')
]

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path(VERSION_1, include(router.urls)),
    path(VERSION_1, include(auth_urls)),
]
