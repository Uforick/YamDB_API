from . import serializers
from rest_framework.mixins import (CreateModelMixin, )
from rest_framework.viewsets import GenericViewSet


class UserCreateMixin(CreateModelMixin, GenericViewSet):
    serializer_class = serializers.EmailForTokenSerialzer
