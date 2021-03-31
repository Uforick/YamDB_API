from rest_framework import serializers

from .models import CustomUser


class EmailForTokenSerialzer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = CustomUser


class MeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('email', 'role')


class EmailConfermeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
