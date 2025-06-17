from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import localtime

User = get_user_model()

class TimeSlot(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    # Para ver el horario en la zona horaria local (localtime)
    def __str__(self):
        start_local = localtime(self.start)
        end_local = localtime(self.end)
        return f"{start_local.strftime('%d/%m/%Y %H:%M')} - {end_local.strftime('%H:%M')}"

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
    
#  Cuando se crea un timeslot, se crean las relaciones con todas las mesas
@receiver(post_save, sender=TimeSlot)
def create_table_time_slots(sender, instance, created, **kwargs):
    if created:
        for table in Table.objects.all():
            TableTimeSlot.objects.get_or_create(table=table, timeslot=instance)