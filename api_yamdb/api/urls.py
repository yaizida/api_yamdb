from rest_framework import routers

from django.urls import path, include

from .views import (UserViewSet, UserMeAPIView,
                    send_confirmation_code, GetAuthTokenSerializer)

app_name = 'api'

VERSION_1 = 'v1/'

auth_urls = [
    path('auth/signup/', send_confirmation_code, name='signup'),
    path('auth/token/', GetAuthTokenSerializer.as_view(), neme='get_token')
]

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path(VERSION_1 + 'users/me/', UserMeAPIView.as_view(), name='self'),
    path(VERSION_1, include(routers.urls)),
    path(VERSION_1, include(auth_urls)),
]
