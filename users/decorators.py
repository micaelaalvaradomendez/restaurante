from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def role_required(*allowed_roles):
    """
    Decorador para verificar múltiples roles permitidos
    Ejemplo de uso: @role_required('ADMIN', 'CAJERO')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
                
            if request.user.rol in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            raise PermissionDenied("No tienes permiso para acceder a esta página")
        return wrapper
    return decorator

def admin_required(view_func):
    """
    Solo para administradores (y superusuarios)
    """
    return role_required('ADMIN')(view_func)

def cashier_required(view_func):
    """
    Para cajeros y administradores
    """
    return role_required('CAJERO', 'ADMIN')(view_func)

def client_required(view_func):
    """
    Solo para clientes
    """
    return role_required('CLIENTE')(view_func)

def admin_or_cashier_required(view_func):
    """
    Para administradores y cajeros (excluye clientes)
    """
    return role_required('ADMIN', 'CAJERO')(view_func)