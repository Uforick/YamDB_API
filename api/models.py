from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import CustomUser

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.SmallIntegerField()
    rating = models.SmallIntegerField(
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
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        db_index=False,
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    text = models.TextField(max_length=5000, blank=False, verbose_name="Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews",
        verbose_name="Автор"
    )
    score = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
    )
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
        db_index=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = (
            "author",
            "title",
        )
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.author} - {self.title}"


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name="Текст")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments",
        verbose_name="Автор"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата публикации"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name="comments",
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)