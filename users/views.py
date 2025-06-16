from django.shortcuts import render, redirect
from users.mixins import ClientRequiredMixin, AdminRequiredMixin, AdminOrCashierRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .mixins import ClientRequiredMixin, AdminRequiredMixin  

class ClientRequired(ClientRequiredMixin):
    def my_reservations(request):
        return render(request, 'reservations/my_reservations.html')
    
    def perfil_usuario(request):
        return render(request, 'perfil.html', {'usuario': request.user})

class AdminRequired(AdminRequiredMixin):
    def admin_dashboard(request):
        return render(request, 'admin/dashboard.html')

class AdminOrCashierRequired(AdminOrCashierRequiredMixin):
    def manage_orders(request):
        return render(request, 'orders/manage.html')

    def some_shared_view(request):
        return render(request, 'shared/view.html')
