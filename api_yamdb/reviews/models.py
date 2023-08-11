from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from reviews.validators import (unicode_username_validator,
                                validate_non_reserved,
                                validate_year)


class User(AbstractUser):

    class UserRoles(models.TextChoices):
        USRER = 'user', ('User')
        MODERATOR = 'moderator', ('Moderator')
        ADMIN = 'admin', ('Admin')

    username = models.CharField(
        unique=True,
        max_length=settings.MAX_LENGTH_FIELDS,
        validators=[unicode_username_validator(), validate_non_reserved],
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.MAX_LENGTH_FIELDS
    )
    role = models.CharField(
        choices=UserRoles.choices,
        default=UserRoles.USRER,
        max_length=settings.MAX_ROLE_LENGHT
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
        return (self.role == self.UserRoles.ADMIN) or self.is_superuser


class BaseCategoryGenre(models.Model):
    """Абстрактная модель для категорий и жанров"""
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
    """Модель категорий"""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategoryGenre):
    """Модель жанров"""
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=[validate_year]
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
