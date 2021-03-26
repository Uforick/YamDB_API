from . import serializers
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.mixins import (CreateModelMixin, )
from rest_framework.viewsets import GenericViewSet
import secrets
import string


def generate_alphanum_crypt_string():
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(12))
    return(crypt_rand_string)


class UserCreateMixin(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.EmailForTokenSerialzer

    def perform_create(self, serializer):
        email = self.request.POST.get('email')
        rand_string = generate_alphanum_crypt_string()
        hashed_password = make_password(rand_string)
        send_mail(
            'Код подтверждения email',
            rand_string,
            'create_profile@yamdb.com',
            [email],
            fail_silently=False,
        )
        serializer.save(password=hashed_password, email=email, username=email)
