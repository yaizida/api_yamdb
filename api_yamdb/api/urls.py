from rest_framework import routers

from django.urls import path, include

from .views import SignupView, UserViewSet, UserMeAPIView

app_name = 'api'

VERSION_1 = 'v1/'

auth_urls = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
]

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path(VERSION_1 + 'users/me/', UserMeAPIView.as_view(), name='self'),
    path(VERSION_1, include(routers.urls)),
    path(VERSION_1, include(auth_urls)),
]
