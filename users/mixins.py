from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class RoleRequiredMixin:
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.rol in self.allowed_roles or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("No tienes permiso para acceder a esta página")

class AdminRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN']

class CashierRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['CAJERO', 'ADMIN']

class ClientRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['CLIENTE']

class AdminOrCashierRequiredMixin(RoleRequiredMixin):
    allowed_roles = ['ADMIN', 'CAJERO']
