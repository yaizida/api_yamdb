"""URL для API."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    CreateUserView,
    UserViewSet,
    GetAuthTokenView
)
VERSION_1 = 'v1/'
auth_urls = [
    path('auth/signup/', CreateUserView.as_view(), name='signup'),
    path('auth/token/', GetAuthTokenView.as_view(), name='token')
]
router = DefaultRouter()
router.register("users", UserViewSet)
router.register('categories', CategoryViewSet, basename='сategories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',
)

urlpatterns = [
    path(VERSION_1, include(router.urls)),
    path(VERSION_1, include(auth_urls)),
]
