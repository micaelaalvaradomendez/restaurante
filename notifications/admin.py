from django.contrib import admin
from .models import Notification, NotificationStatus

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'created_at')
    search_fields = ('title', 'message', 'sender__username')

@admin.register(NotificationStatus)
class NotificationStatusAdmin(admin.ModelAdmin):
    list_display = ('notification', 'user', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'notification__title')
