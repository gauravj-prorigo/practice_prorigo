from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home.views import BlogViewSet, TaskViewSet, RegisterView, RoleAssignView, MeView,UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blog')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/me/', MeView.as_view(), name='me'),
    path('api/users/<int:pk>/role/', RoleAssignView.as_view(), name='role-assign'),
    path('api/', include(router.urls)),
]
