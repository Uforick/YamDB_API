from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .fields import TitleNestedField
from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = TitleNestedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
    )
    category = TitleNestedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        request = self.context['request']
        title_id = request.parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title,
                author=request.user,
            ).exists():
                raise serializers.ValidationError('Only one review is allowed')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', many=False
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
