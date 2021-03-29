from rest_framework.serializers import SlugRelatedField


class TitleNestedField(SlugRelatedField):
    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{self.slug_field: data})
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        out = {
            'name': value.name,
            'slug': value.slug
        }
        return out
