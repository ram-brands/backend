from rest_framework.permissions import SAFE_METHODS, BasePermission


class ObjectOwnership(BasePermission):
    def has_object_permission(self, request, view, obj=None):
        return (obj is not None) and (request.user in obj.owners)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
