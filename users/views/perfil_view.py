from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from bookings.models import Booking

## Pasar a Class Based View 
@login_required
def perfil_view(request):
    usuario = request.user
    reservas = Booking.objects.filter(user=usuario).select_related('table', 'timeslot')

    reservas_en_curso = reservas.filter(timeslot__end__gte=now()).order_by('timeslot__start')
    reservas_historicas = reservas.filter(timeslot__end__lt=now()).order_by('-timeslot__start')

    return render(request, 'perfil.html', {
        'usuario': usuario,
        'reservas_en_curso': reservas_en_curso,
        'reservas_historicas': reservas_historicas
    })
