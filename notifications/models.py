from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipients = models.ManyToManyField(User, through='NotificationStatus', related_name='notifications') # Relaciona usuarios con notificaciones
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class NotificationStatus(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'notification')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.notification} - Read: {self.is_read}"
    
#Cuando se crea una notificación, se crean los estados de notificación para los usuarios correspondientes
@receiver(post_save, sender=Notification)
def create_notification_status(sender, instance, created, **kwargs):
    if created:
        if instance.is_global:
            # Notificación general: para todos los usuarios
            for user in User.objects.all():
                NotificationStatus.objects.get_or_create(user=user, notification=instance)
        else:
            # Notificación individual: para los destinatarios seleccionados
            for user in instance.recipients.all():
                NotificationStatus.objects.get_or_create(user=user, notification=instance)