from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking
from .forms import BookingForm
from django.shortcuts import render
from django.db.models import Max

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        # Solo permite una reserva pendiente por usuario (no aprobada)
        if Booking.objects.filter(user=self.request.user, is_approved=False).exists():
            form.add_error(None, "Ya tienes una reserva pendiente de respuesta.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.is_approved = False

        Ultimo_id = Booking.objects.aggregate(max_id=Max('id'))['max_id'] or 0
        next_id = Ultimo_id + 1
        form.instance.code = f"RES{next_id:04d}"

        return super().form_valid(form)

 