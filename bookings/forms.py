from django import forms
from .models import Booking, Table, TimeSlot

class TimeSlotModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Muestra fecha y hora: 01/06/2025 20:00 - 01/06/2025 21:00
        return f"{obj.start.strftime('%d/%m/%Y %H:%M')} - {obj.end.strftime('%H:%M')}"

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