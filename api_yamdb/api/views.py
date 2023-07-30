from rest_framework import viewsets

from reviews.models import Category, Genre, Title, Review, Comment
from .mixins import CategoryGenreMixinSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitleEditSerializer,
    ReviewSerializer,
    CommentSerializer
)


class CategoryViewSet(CategoryGenreMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleEditSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
