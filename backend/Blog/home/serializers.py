# blogapp/serializers.py
from rest_framework import serializers
from .models import Blog, Task
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        # create_user handles password hashing
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class RoleAssignSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[('user','User'), ('employee','Employee'), ('admin','Admin'),  ('maneger', 'Maneger'),])


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at']
        read_only_fields = ['id', 'created_at']