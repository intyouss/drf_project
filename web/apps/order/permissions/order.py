from rest_framework import permissions


class OrderPermission(permissions.BasePermission):
    """订单权限限制"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
