from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, NotificationStatusViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'status', NotificationStatusViewSet, basename='notificationstatus')

urlpatterns = [
    path('', include(router.urls)),
]
