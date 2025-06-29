from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from menu_app.models import Product, Category
from bookings.models import Booking, Table, TimeSlot
from orders.models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .mixins import StaffRequiredMixin
from bookings.models import TimeSlot
from notifications.models import Notification
from django.contrib import messages
from django.forms import inlineformset_factory
from orders.models import Order

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem,
    fields=['product', 'quantity', 'price_at_purchase'],
    extra=1, can_delete=True
)

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'ADMIN'

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol in ['ADMIN', 'CAJERO']

class AdminDashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_bookings'] = Booking.objects.filter(is_approved=False, is_rejected=False).count()
        context['pending_orders'] = Order.objects.filter(state='PREPARACION').count()
        return context

class BookingListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Booking
    template_name = "custom_admin/booking_list.html"
    context_object_name = "bookings"
    paginate_by = 20  

    def get_queryset(self):
        return Booking.objects.all().order_by('-approved_date')

class OrderListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Order
    template_name = 'custom_admin/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.all().order_by('-id')

class OrderDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Order
    template_name = 'custom_admin/order_detail.html'
    context_object_name = 'order'

class OrderUpdateStateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.state = 'ENVIADO'
        order.save()
        return redirect('custom_admin:order_list')

class OrderCreateView(CreateView):
    model = Order
    fields = ['user', 'state']
    template_name = 'custom_admin/order_edit.html'
    success_url = reverse_lazy('custom_admin:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
        else:
            context['formset'] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            carrito = {}
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    producto = item_form.cleaned_data['product']
                    cantidad = item_form.cleaned_data['quantity']
                    carrito[producto.id] = cantidad
            cliente = form.cleaned_data['user']
            pedido = Order.objects.crear_pedido_desde_carrito(cliente, carrito)
            pedido.confirmado = True
            pedido.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['state']
    template_name = 'custom_admin/order_edit.html'
    success_url = reverse_lazy('custom_admin:order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'custom_admin/order_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:order_list')

class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Product
    template_name = "custom_admin/product_list.html"
    context_object_name = "products"

class TableView(AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        return context

class TableManagementView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Table
    template_name = "custom_admin/table_management.html"
    context_object_name = "tables"

class TableUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Table
    fields = ['capacity', 'description']
    template_name = 'custom_admin/table_form.html'
    success_url = reverse_lazy('custom_admin:table_management')

class TableDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Table
    template_name = 'custom_admin/table_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:table_management')

class TableCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Table
    fields = ['capacity', 'description']
    template_name = 'custom_admin/table_form.html'
    success_url = reverse_lazy('custom_admin:table_management')

class BookingApproveView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.is_approved = True
        booking.save()
        return redirect('custom_admin:booking_list')

class BookingRejectView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        booking.is_rejected = True
        booking.save()
        return redirect('custom_admin:booking_list')

class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'quantity', 'image', 'categories', 'is_available']  # Ajusta según tu modelo
    template_name = 'custom_admin/product_form.html'
    success_url = reverse_lazy('custom_admin:product_list')

class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'quantity', 'image', 'categories', 'is_available']
    template_name = 'custom_admin/product_form.html'
    success_url = reverse_lazy('custom_admin:product_list')

class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'custom_admin/product_confirm_delete.html'
    success_url = reverse_lazy('custom_admin:product_list')

class TimeSlotListView(ListView):
    model = TimeSlot
    template_name = "custom_admin/timeslot_list.html"
    context_object_name = "timeslots"

class TimeSlotCreateView(CreateView):
    model = TimeSlot
    fields = ['start', 'end']
    template_name = "custom_admin/timeslot_form.html"
    success_url = reverse_lazy('custom_admin:timeslot_list')

class TimeSlotUpdateView(UpdateView):
    model = TimeSlot
    fields = ['start', 'end']
    template_name = "custom_admin/timeslot_form.html"
    success_url = reverse_lazy('custom_admin:timeslot_list')

class TimeSlotDeleteView(DeleteView):
    model = TimeSlot
    template_name = "custom_admin/timeslot_confirm_delete.html"
    success_url = reverse_lazy('custom_admin:timeslot_list')
 
class NotificacionAdminListView(ListView):
    model = Notification
    template_name = "custom_admin/notifications_admin_list.html"
    context_object_name = "notificaciones"

class NotificacionAdminCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Notification
    fields = ['title', 'message', 'is_global', 'recipients']
    template_name = "custom_admin/notifications_admin_form.html"
    success_url = reverse_lazy('custom_admin:notificaciones_admin')

    def form_valid(self, form):
        form.instance.sender = self.request.user  # Asigna el usuario actual como sender
        return super().form_valid(form)

class NotificacionAdminUpdateView(UpdateView):
    model = Notification
    fields = ['title', 'message', 'is_global', 'recipients']
    template_name = "custom_admin/notifications_admin_form.html"
    success_url = reverse_lazy('custom_admin:notificaciones_admin')

class NotificacionAdminDeleteView(DeleteView):
    model = Notification
    template_name = "custom_admin/notifications_admin_confirm_delete.html"
    success_url = reverse_lazy('custom_admin:notificaciones_admin')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "custom_admin/category_confirm_delete.html"
    success_url = reverse_lazy('custom_admin:category_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Verifica si hay productos asociados ANTES de borrar
        if self.object.products.exists():
            messages.error(request, "No se puede eliminar la categoría porque tiene productos asociados.")
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

class CategoryListView(ListView):
    model = Category
    template_name = "custom_admin/category_list.html"
    context_object_name = "object_list"

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'description', 'is_active']
    template_name = "custom_admin/category_form.html"
    success_url = reverse_lazy('custom_admin:category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description', 'is_active']
    template_name = "custom_admin/category_form.html"
    success_url = reverse_lazy('custom_admin:category_list')

class CarritoOrdenView(LoginRequiredMixin, View):
    def post(self, request):
        carrito = request.session.get('carrito', [])
        usuario = request.user

        Order.objects.crear_pedido_desde_carrito(usuario, carrito)
        
        messages.success(request, "El pedido ha sido creado exitosamente.")
        return redirect('nombre_de_la_vista_de_redireccion')  # Cambia esto a la vista a la que quieras redirigir después de crear el pedido

def confirmar_pedido_admin(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('custom_admin:order_list')
    pedido = Order.objects.crear_pedido_desde_carrito(request.user, carrito)
    pedido.confirmado = True
    pedido.save()
    request.session['carrito'] = {}
    return redirect('custom_admin:order_list')