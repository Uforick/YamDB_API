from rest_framework import serializers
from .models import CustomUser


class EmailForTokenSerialzer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', )
        model = CustomUser
