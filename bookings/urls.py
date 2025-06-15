from django.urls import path
from .views import BookingCreateView

urlpatterns = [
    path('reservar/', BookingCreateView.as_view(), name='crear_reserva'),
]
