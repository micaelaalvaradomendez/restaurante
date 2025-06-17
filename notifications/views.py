from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationStatus
from .serializers import NotificationSerializer, NotificationStatusSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminForStatus
from django.contrib.auth.mixins import LoginRequiredMixin

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly] # Permite a los administradores crear y ver notificaciones, pero solo lectura para usuarios normales(Clientes)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class NotificationStatusViewSet(viewsets.ModelViewSet):
    queryset = NotificationStatus.objects.all()
    serializer_class = NotificationStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForStatus] # Permite a los usuarios ver y actualizar sus propios estados de notificación, o a los administradores ver todos los estados
    http_method_names = ['get', 'put']  # Solo permite lectura y actualización
    def get_queryset(self):
        # Que un usuario solo vea sus propios estados, admins ven todos
        user = self.request.user
        if user.is_staff:
            return NotificationStatus.objects.all()
        return NotificationStatus.objects.filter(user=user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para modificar este estado")
        serializer.save()

class NotisUsuario(LoginRequiredMixin):

    def lista_notificaciones(request):
        notificaciones_estado_lista = NotificationStatus.objects.filter(user=request.user)
        return render(request, 'notifications/notifications.html', {
            'notificaciones_estado_lista': notificaciones_estado_lista
        })

    def marcar_leida(request, pk):
        estado = get_object_or_404(NotificationStatus, pk=pk, user=request.user)
        if request.method ==  'POST':
            estado.is_read = True
            estado.save()
        return redirect('mis_notificaciones')