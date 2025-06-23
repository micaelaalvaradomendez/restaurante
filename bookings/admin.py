from django.contrib import admin
from .models import Booking, Table, TimeSlot;

admin.site.register(Booking)
admin.site.register(Table)
admin.site.register(TimeSlot)
