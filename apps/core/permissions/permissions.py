from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.models import Role


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if user.role and user.role.name == Role.RoleName.MANAGER:
            return True

        return getattr(
            obj,
            'owner',
            getattr(obj, 'user', None)
        ) == user

class IsImageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.listing.owner == request.user

class HasPermissionCodename(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated or not user.is_active:
            return False
        #Адміністратор завжди може все, йому дозволи не потрібні
        if user.is_superuser:
            return True

        #Витягуємо з в'юшки ім'я пермішина на перевірку
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return False

        #Ліземо в БД і перевіряємо, чи є у ролі користувача цей codename
        if user.role_id is None:
            return False

        return user.role.permissions.filter(
            codename=required_permission
        ).exists()

class HasPermissionCodenameOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return HasPermissionCodename().has_permission(request, view)
