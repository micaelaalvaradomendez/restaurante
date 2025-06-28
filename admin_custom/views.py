from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from menu_app.models import Product, Category
from bookings.models import Booking, Table, TimeSlot
from orders.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .mixins import StaffRequiredMixin
from bookings.models import TimeSlot
from notifications.models import Notification

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