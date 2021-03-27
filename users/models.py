from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        role=None,
        username=None,
        first_name=None,
        last_name=None,
        bio=None
    ):
        user = self.model(
            email=email,
            password=password,
            role=role,
            username=username,
            first_name=first_name,
            last_name=last_name,
            bio=bio
        )
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        password=None,
        username=None,
        first_name=None,
        last_name=None,
        bio=None
    ):
        user = self.create_user(
            email=email,
            password=password,
            role='admin',
            username=username,
            first_name=first_name,
            last_name=last_name,
            bio=bio
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        USR = 'user', ('user')
        MOD = 'moderator', ('moderator')
        ADM = 'admin', ('admin')
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=30,
                            choices=Roles.choices,
                            default=Roles.USR,
                            verbose_name='Роль'
                            )
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(
        max_length=30,
        null=True,
        # blank=True,
        unique=True,
    )
    # is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Roles.ADM

    @property
    def is_moderator(self):
        return self.role == self.Roles.MOD

    @property
    def is_user(self):
        return self.role == self.Roles.USR

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        ordering = ('email',)

    def __str__(self):
        return self.email
