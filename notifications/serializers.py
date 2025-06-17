from rest_framework import serializers
from .models import Notification, NotificationStatus

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'title', 'message', 'created_at']

class NotificationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationStatus
        fields = ['id', 'notification', 'user', 'is_read', 'created_at']
        read_only_fields = ['notification', 'user', 'created_at']

    def update(self, instance, validated_data):
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
