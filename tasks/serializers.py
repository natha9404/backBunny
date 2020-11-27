from rest_framework import serializers
from .models import User_Tasks
from users.serializers import UserSerializer

class User_TasksSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = User_Tasks
        fields = '__all__'