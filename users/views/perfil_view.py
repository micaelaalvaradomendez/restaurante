from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from bookings.models import Booking
from orders.models import OrderItem
from menu_app.models import Product, Rating

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        reservas = Booking.objects.filter(user=usuario).select_related('table', 'timeslot')

        reservas_pendientes = reservas.filter(
            is_approved=False
        ) | reservas.filter(
            timeslot__start__gt=now()
        )
        reservas_pendientes = reservas_pendientes.distinct().order_by('timeslot__start')

        reservas_historicas = reservas.filter(
            is_approved=True,
            timeslot__start__lte=now()
        ).order_by('-timeslot__start')

        productos_entregados = Product.objects.filter(
            orderitem__order__user=usuario,
            orderitem__order__state__in=["RETIRADO", "ENVIADO"]
        ).distinct()

        productos_calificados = Product.objects.filter(rating__user=usuario)
        productos_para_calificar = productos_entregados.exclude(id__in=productos_calificados)
        context['productos_para_calificar'] = productos_para_calificar

        context['calificaciones'] = Rating.objects.filter(user=usuario).select_related('product')

        context['usuario'] = usuario
        context['reservas_pendientes'] = reservas_pendientes
        context['reservas_historicas'] = reservas_historicas
        return context
