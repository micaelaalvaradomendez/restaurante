from django.core.exceptions import PermissionDenied

class ClientRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_cliente:
            raise PermissionDenied(redirect_url='users:login')
        return super().dispatch(request, *args, **kwargs)