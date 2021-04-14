from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_brand_or_super = request.user.is_authenticated and (request.user.is_brand or request.user.is_superuser)
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            return is_brand_or_super
        elif request.method == 'PUT' or request.method == 'PATCH':
            return is_brand_or_super
        elif request.method == 'DELETE':
            return is_brand_or_super

        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.can_read_by(request.user)
        elif request.method == 'POST':
            return obj.can_create_by(request.user)
        elif request.method == 'PUT' or request.method == 'PATCH':
            return obj.can_update_by(request.user)
        elif request.method == 'DELETE':
            return obj.can_delete_by(request.user)

        return False
