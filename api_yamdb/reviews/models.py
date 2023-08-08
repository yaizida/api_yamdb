from datetime import date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from reviews.validators import (UsernameRegexValidator, validate_non_reserved)
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):

    class UserRoles(models.TextChoices):
        USRER = 'user', ('User')
        MODERATOR = 'moderator', ('Moderator')
        ADMIN = 'admin', ('Admin')

    username = models.CharField(
        unique=True,
        max_length=settings.MAX_LENGTH_FIELDS,
        validators=[UsernameRegexValidator(), validate_non_reserved],
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.MAX_LENGTH_FIELDS
    )
    role = models.CharField(
        choices=UserRoles.choices,
        default=UserRoles.USRER,
        max_length=10
    )
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH_FIELDS,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH_FIELDS,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR or self.is_staff

    @property
    def is_admin(self):
        return ((self.role == self.UserRoles.ADMIN) or self.is_superuser
                or self.is_staff)


class BaseCategoryGenre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseCategoryGenre):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=[
            MaxValueValidator(
                date.today().year,
                message='Год создания не может быть позже нынешнего'
            ),
        ]
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title'
    )


class ReviewCommentBase(models.Model):
    """Абстрактная модель для отзывов и комментариев"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True


class Review(ReviewCommentBase):
    """Модель отзывов к произведениям"""
    SCORE_ERROR_MESSAGE = "Оценка должна быть в диапазоне от 1 до 10"

    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        blank=False,
        validators=[
            MinValueValidator(1, message=SCORE_ERROR_MESSAGE),
            MaxValueValidator(10, message=SCORE_ERROR_MESSAGE)
        ]
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(ReviewCommentBase):
    """Модель комментариев к отзывам"""
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(ReviewCommentBase.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
