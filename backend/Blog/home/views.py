# blogapp/views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import BlogSerializer, TaskSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Blog, Task
from .serializers import (
    RegisterSerializer, UserSerializer,
    RoleAssignSerializer, BlogSerializer, TaskSerializer
)
from .permissions import BlogPermission, IsAdminRole

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]  # change to IsAuthenticated when you enable auth

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  # change later for auth




User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]   # anyone can register

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class RoleAssignView(APIView):
    permission_classes = [IsAdminRole]

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = RoleAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_role = serializer.validated_data['role']

        # optional safety: prevent demoting last super-admin (not implemented here)
        user.role = new_role
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated, BlogPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin-only endpoint to list and retrieve users.
    ReadOnlyModelViewSet provides `list` and `retrieve`.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]