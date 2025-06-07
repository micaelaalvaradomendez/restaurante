from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from menu_app.models import Product, Category
from bookings.models import Booking, Table
from orders.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .mixins import StaffRequiredMixin

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
        context['pending_bookings'] = Booking.objects.filter(is_approved=False).count()
        context['pending_orders'] = Order.objects.filter(state='PREPARACION').count()
        return context

class BookingListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Booking
    template_name = "custom_admin/booking_list.html"
    context_object_name = "bookings"
    paginate_by = 20  # Opcional: paginación

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

@login_required
@require_POST
def approve_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_approved = True
    booking.save()
    return redirect('custom_admin:booking_list')

@login_required
@require_POST
def reject_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_approved = False
    booking.save()
    return redirect('custom_admin:booking_list')

from django.views.generic import CreateView, UpdateView, DeleteView
from menu_app.models import Product

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

@require_POST
@login_required
def order_update_state(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.state = 'ENTREGADO'
    order.save()
    return redirect('custom_admin:order_list')