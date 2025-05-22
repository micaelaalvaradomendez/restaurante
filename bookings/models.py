from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeSlot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start} - {self.end}"

class Table(models.Model):
    capacity = models.IntegerField()
    description = models.CharField(max_length=200)
    is_reserved = models.BooleanField(default=False)
    time_slots = models.ManyToManyField(TimeSlot)  # Mesa disponible en varias franjas

    def __str__(self):
        return f"Mesa #{self.id} (Capacidad: {self.capacity})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    is_approved = models.BooleanField(default=False)
    approved_date = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True)

    def __str__(self):
        return f"Reserva #{self.code} - {self.user.username}"