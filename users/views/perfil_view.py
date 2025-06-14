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
        productos_pedidos = Product.objects.filter(orderitem__order__user=usuario).distinct()
        productos_calificados = Product.objects.filter(rating__user=usuario)

        context['usuario'] = usuario
        context['reservas_en_curso'] = reservas.filter(timeslot__end__gte=now()).order_by('timeslot__start')
        context['reservas_historicas'] = reservas.filter(timeslot__end__lt=now()).order_by('-timeslot__start')
        context['calificaciones'] = Rating.objects.filter(user=usuario).select_related('product')
        context['productos_para_calificar'] = productos_pedidos.exclude(id__in=productos_calificados)
        return context
