from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from decimal import Decimal
from django.contrib import messages

from .models import Order
from menu_app.models import Product
from .forms import PaymentForm
from .service import process_payment

class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if not product.is_available:
            # You can add a Django message here to inform the user
            return redirect('menu_por_categorias')
        
        carrito = request.session.get('carrito', {})
        # Ensure the product ID is a string for session consistency
        carrito[str(product_id)] = carrito.get(str(product_id), 0) + 1
        request.session['carrito'] = carrito
        
        # Redirect back to the previous page (the menu)
        return redirect(request.META.get('HTTP_REFERER', 'menu_por_categorias'))

class VerCarritoView(TemplateView):
    template_name = 'menu/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrito = self.request.session.get('carrito', {})
        product_ids = carrito.keys()
        productos = Product.objects.filter(id__in=product_ids)
        
        context['productos'] = productos
        context['carrito'] = carrito
        return context

class ConfirmarPedidoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('menu_por_categorias')
        
        order = Order.objects.crear_pedido_desde_carrito(request.user, carrito)
        
        # Vaciar el carrito y notificar al usuario
        request.session['carrito'] = {}
        messages.success(request, f"Tu pedido #{order.code} ha sido recibido. Te notificaremos cuando sea aprobado y puedas proceder con el pago.")
        
        return redirect('orders:mis_pedidos')

class MisPedidosView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/mis_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-buy_date')

class PaymentView(LoginRequiredMixin, FormView):
    template_name = 'orders/payment_form.html'
    form_class = PaymentForm

    def dispatch(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        
        if order.state != 'APROBADO':
            messages.error(request, "Este pedido no se puede pagar en este momento.")
            return redirect('orders:mis_pedidos')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)
        context['order'] = order
        return context

    def form_valid(self, form):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(Order, id=order_id, user=self.request.user)

        payment_successful = process_payment(order=order, card_details=form.cleaned_data)

        if payment_successful:
            order.state = 'PREPARACION'
            
            # Actualizar el stock del producto AHORA que el pago fue exitoso
            for item in order.orderitem_set.all():
                product = item.product
                product.quantity -= item.quantity
                if product.quantity <= 0:
                    product.is_available = False
                product.save()

            order.save() # Guardar el estado final del pedido
            self.request.session['carrito'] = {}
            return redirect('orders:payment_success', order_id=order.id)
        
        form.add_error(None, "No se pudo procesar el pago. Intente de nuevo.")
        return self.form_invalid(form)

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs.get('order_id')
        context['order'] = get_object_or_404(Order, id=order_id, user=self.request.user)
        return context