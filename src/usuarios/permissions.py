
#IMPORTANTE EN LA DB TENER TRES GROUPS CARGADOS PARA QUE FUNCIONEN LOS PERMISOS.
#SE DEBE CARGAR MANUALMENTE ROL DE Cliente Y Vendedor


from rest_framework import permissions

class PermissionVendedor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Permitir superusuarios
        if request.user.is_superuser:
            return True
        # Permitir grupos específicos (minúsculas para coincidir con JWT)
        return request.user.groups.filter(name__in=['admin', 'administrador', 'vendedor']).exists()

class PermissionCliente(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name__in=['cliente', 'vendedor']).exists()