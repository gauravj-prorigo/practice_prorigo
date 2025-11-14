from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    """Allow only users with role 'admin' or is_superuser."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or getattr(user, 'role', None) == 'admin'

class BlogPermission(BasePermission):
    """
    - GET (safe): authenticated users can view
    - POST: employee or admin
    - PUT/PATCH: admin can edit any; employee only own; user none
    - DELETE: admin only
    """
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # allow reads for any authenticated user
        if request.method in SAFE_METHODS:
            return True
        # create
        if request.method == 'POST':
            return user.is_superuser or getattr(user, 'role', None) in ('employee','admin')
        # other methods: let object-level permission decide
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        if user.is_superuser or getattr(user, 'role', None) == 'admin':
            return True
        role = getattr(user, 'role', None)
        if request.method in ('PUT','PATCH'):
            if role == 'employee':
                return getattr(obj, 'author', None) == user
            return False
        if request.method == 'DELETE':
            return False  # only admin (already handled above)
        return False
