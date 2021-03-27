from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters, permissions
from rest_framework.decorators import action
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
    permission_classes = [permissions.IsAdminOrReadOnly]
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
    permission_classes = [permissions.IsAdminOrReadOnly]
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
    permission_classes = [permissions.IsAdminOrReadOnly]
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
    

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        # queryset = get_object_or_404(User, username=self.kwargs.get('username'))
        me = get_object_or_404(User, username=request.user.username)
        serializer = serializers.MeSerializer(me, data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save(data=request.data)

        return Response(serializer.data)



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
