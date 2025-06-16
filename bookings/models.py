from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeSlot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        # Ejemplo: 01/06/2025 20:00 - 21:00
        return f"{self.start.strftime('%d/%m/%Y %H:%M')} - {self.end.strftime('%H:%M')}"

class Table(models.Model):
    capacity = models.IntegerField(verbose_name="Capacidad")
    description = models.CharField(max_length=200, verbose_name="Descripción")
    time_slots = models.ManyToManyField(TimeSlot, through='TableTimeSlot', verbose_name="Horarios")

    def __str__(self):
        return f"Mesa #{self.id} (Capacidad: {self.capacity})"

    def is_available(self):
        # Devuelve True si hay al menos un timeslot no reservado
        return self.tabletimeslot_set.filter(is_reserved=False).exists()

class TableTimeSlot(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('table', 'timeslot')

    def __str__(self):
        return f"Mesa {self.table.id} - {self.timeslot} - Reservada: {self.is_reserved}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    is_approved = models.BooleanField(default=False)
    approved_date = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True)

    def __str__(self):
        return f"Reserva #{self.code} - {self.user.username}"