from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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
