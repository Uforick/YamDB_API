from django.db.models import Avg
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import permissions, serializers
from .models import Categories, Comment, Genres, Review, Titles, User
from .permissions import IsAdmin, IsModerator, IsOwner, ReadOnly


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
        me = get_object_or_404(User, username=request.user.username)
        serializer = serializers.MeSerializer(me, data=request.data,)
        serializer.is_valid(raise_exception=True)
        serializer.save(data=request.data)

        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs["title_id"])
        return title.reviews.all()


    def avg_score(self, title):
        avg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)
        self.avg_score(title)

    def perform_update(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)
        self.avg_score(title)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs["review_id"])
        return review.comments.all()


    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
