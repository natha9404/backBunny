from rest_framework import serializers
from .models import OwnUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnUser
        fields = '__all__'