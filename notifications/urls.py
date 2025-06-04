from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import NotificationViewSet, NotificationStatusViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'status', NotificationStatusViewSet, basename='notificationstatus')

urlpatterns = [
    path('', include(router.urls)),
    path('mis-notificaciones/',views.lista_notificaciones, name='mis_notificaciones'),
    path('marcar-leida/<int:pk>/', views.marcar_leida, name='marcar_leida'),
]
