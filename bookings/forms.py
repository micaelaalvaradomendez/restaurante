from django import forms
from .models import Booking, Table, TimeSlot

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['table', 'timeslot', 'observations']
        widgets = {
            'table': forms.Select(attrs={'class': 'form-select'}),
            'timeslot': forms.Select(attrs={'class': 'form-select'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'table': 'Mesa',
            'timeslot': 'Horario',
            'observations': 'Observaciones',
        }