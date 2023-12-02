from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='модератор').exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return request.method in ['GET', 'PUT', 'PATCH', 'DELETE']
        return False
