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
from .models import Category, Comment, Genre, Review, Title, User
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


class UsersViewSet(CustomViewSet, RetrieveModelMixin, UpdateModelMixin):
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
        queryset = Review.objects.all()
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if title is not None:
            queryset = Review.objects.filter(title=self.kwargs.get('title_id'))
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])

        if Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists():
            raise exceptions.ValidationError('Вы уже оставили отзыв')
        serializer.save(author=self.request.user, title=title)

        avg_score = Review.objects.filter(title=title).aggregate(Avg('score'))

        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)
        avg_score = Review.objects.filter(title=title).aggregate(Avg('score'))

        title.rating = avg_score['score__avg']
        title.save(update_fields=['rating'])


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated | ReadOnly,
                          IsOwner | IsAdmin | IsModerator | ReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.all()
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        if review is not None:
            queryset = Comment.objects.filter(
                review=self.kwargs.get('review_id')
            )
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)
