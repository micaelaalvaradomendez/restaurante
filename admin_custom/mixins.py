from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'rol', None) != 'ADMIN':
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

class StaffRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'rol', None) not in ['ADMIN', 'CAJERO']:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)