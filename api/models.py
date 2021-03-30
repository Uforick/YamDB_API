import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


def validate_year(value):
    max_year = datetime.date.today().year + 10
    params = {'value': max_year}
    message = _('Введите год меньше, чем %(value)s')
    if value > max_year:
        raise ValidationError(message=message, params=params)


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
    )

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            validate_year,
        ],
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(max_length=5000, blank=False, verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = (
            'author',
            'title',
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author} - {self.title}'


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Дата публикации'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
