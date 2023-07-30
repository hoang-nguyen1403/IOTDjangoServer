from rest_framework.permissions import BasePermission

class IsAccessed(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.User.filter(id=request.user.id).exists()