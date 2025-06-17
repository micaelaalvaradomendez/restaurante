from django import forms
from .models import Booking, Table, TimeSlot
from django.utils.timezone import localtime

class TimeSlotModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        start_local = localtime(obj.start)
        end_local = localtime(obj.end)
        return f"{start_local.strftime('%d/%m/%Y %H:%M')} - {end_local.strftime('%H:%M')}"

class BookingForm(forms.ModelForm):
    timeslot = TimeSlotModelChoiceField(
        queryset=TimeSlot.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Horario'
    )

    class Meta:
        model = Booking
        fields = ['table', 'timeslot', 'observations']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-select'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'table': 'Mesa',
            'timeslot': 'Horario',
            'observations': 'Observaciones',
        }