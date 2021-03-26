from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404

from . import serializers, permissions
from .models import Categories, Genres, Titles, User


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ['year']


class CategoriesViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer
    permission_classes = []
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GengresViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = Genres.objects.all()
    serializer_class = serializers.GenresSerializer
    permission_classes = []
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitlesViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    queryset = Titles.objects.all()
    serializer_class = serializers.TitlesSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class UsersViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminOnly, ]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]

    def perform_update(self, serializer):

        serializer.save()


# class MeViewSet(
#     ListModelMixin,
#     GenericViewSet,
#     RetrieveModelMixin,
#     UpdateModelMixin
# ):
#     serializer_class = serializers.UserSerializer
#     # permission_classes = [permissions.IsOwnerOnly, ]

#     def get_queryset(self):
#         queryset = get_object_or_404(User, pk=self.kwargs.get('username'))
#         return queryset
