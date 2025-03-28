from rest_framework.permissions import BasePermission, SAFE_METHODS


class AlmacenPermission(BasePermission):
    def has_permission(self, request, view):
        is_safe = request.method in SAFE_METHODS
        is_authenticated = request.user and request.user.is_authenticated

        if is_authenticated:
            try:
                is_editor = request.user.caracteristicas.is_editor
            except Exception:
                print("user dosen't have caracteristicas defined")
                is_editor = False
            if is_safe:
                return True
            if is_editor:
                return True
        return False
