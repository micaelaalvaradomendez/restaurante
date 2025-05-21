from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationStatus
from .serializers import NotificationSerializer, NotificationStatusSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdminForStatus

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class NotificationStatusViewSet(viewsets.ModelViewSet):
    queryset = NotificationStatus.objects.all()
    serializer_class = NotificationStatusSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForStatus]

    def get_queryset(self):
        # Que un usuario solo vea sus propios estados, admins ven todos
        user = self.request.user
        if user.is_staff:
            return NotificationStatus.objects.all()
        return NotificationStatus.objects.filter(user=user)

    def perform_update(self, serializer):
        # Solo actualizar is_read y solo para el usuario dueño
        instance = self.get_object()
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("No tienes permiso para modificar este estado")
        serializer.save()
