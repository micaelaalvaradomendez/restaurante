from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipients = models.ManyToManyField(User, through='NotificationStatus', related_name='notifications')

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