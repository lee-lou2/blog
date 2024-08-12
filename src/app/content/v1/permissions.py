from rest_framework.permissions import IsAuthenticated


class ContentUpdatePermission(IsAuthenticated):
    def has_permission(self, request, view):
        permission = super().has_permission(request, view)
        if not hasattr(request.user, "profile"):
            return False
        return permission
