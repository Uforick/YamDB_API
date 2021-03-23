from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
