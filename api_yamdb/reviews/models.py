from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES_CHOICES = (
    ('admin', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
    )
    email = models.EmailField(
        unique=True,
        max_length=150,
    )
    role = models.CharField(
        choices=ROLES_CHOICES,
        default=settings.DEFAULT_USER,
        max_length=max(len(role) for role, _ in ROLES_CHOICES)
    )
    bio = models.TextField(blank=True, null=True)
    confirmation_code = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=150,
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
        pass

    @property
    def is_admin(self):
        pass


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    yaer = models.IntegerField('Год выпуска')
    description = models.TextField(
        verbose_name='Описание',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
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
