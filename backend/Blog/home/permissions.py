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
    Rules implemented here:

    - SAFE_METHODS (GET/HEAD/OPTIONS): any authenticated user can read.
    - POST (create): allowed only for admin or employee (NOT manager).
    - PUT/PATCH (update): allowed for:
        * superuser
        * admin
        * manager  -> manager can edit any post
        * employee -> only if employee is the author (owner)
    - DELETE: allowed only for admin (and superuser).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Allow reads for any authenticated user
        if request.method in SAFE_METHODS:
            return True

        # Create: only admin or employee (manager cannot create)
        if request.method == 'POST':
            return user.is_superuser or getattr(user, 'role', None) in ('admin', 'employee')

        # For PUT/PATCH/DELETE we let object-level permission decide
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Reads allowed
        if request.method in SAFE_METHODS:
            return True

        # Superuser or admin can do anything (including delete)
        if user.is_superuser or getattr(user, 'role', None) == 'admin':
            return True

        role = getattr(user, 'role', None)

        # Update: manager can edit any; employee can edit only own; others cannot
        if request.method in ('PUT', 'PATCH'):
            if role == 'manager':
                return True
            if role == 'employee':
                return getattr(obj, 'author', None) == user
            return False

        # Delete: only admin/superuser allowed (we already returned True above for them)
        if request.method == 'DELETE':
            return False

        return False
