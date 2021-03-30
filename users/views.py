import secrets
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.views import CustomViewSet

from . import permissions, serializers
from .models import CustomUser as User


def generate_alphanum_crypt_string():
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(12))
    return(crypt_rand_string)


class UserCreateMixin(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.EmailForTokenSerialzer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        email = self.request.POST.get('email')
        rand_string = generate_alphanum_crypt_string()
        hashed_password = make_password(rand_string)
        send_mail(
            'Код подтверждения email',
            rand_string,
            settings.CORE_EMAIL_ADRESS,
            [email],
            fail_silently=False,
        )
        serializer.save(password=hashed_password, email=email, username=email)


class UsersViewSet(CustomViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminOnly]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        me = get_object_or_404(User, username=request.user.username)
        serializer = serializers.MeSerializer(me, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(data=request.data)

        return Response(serializer.data)
