from django.db.models import Avg
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import permissions, serializers
from .models import Category, Genre, Review, Title
from .permissions import IsAdmin, IsModerator, IsOwner, ReadOnly


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['year']


class CustomViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    pass


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(CategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]


class TitleViewSet(CustomViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        queryset = Review.objects.all()
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if title is not None:
            queryset = Review.objects.filter(title=self.kwargs.get('title_id'))
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])



    def avg_score(self, title):
        avg_score = Review.objects.filter(title=title).aggregate(Avg('score'))
        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])

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
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
