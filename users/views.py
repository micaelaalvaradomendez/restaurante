from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required, cashier_required, client_required, admin_or_cashier_required, role_required
from django.contrib.auth.forms import UserCreationForm

@admin_required
def admin_dashboard(request):
    # Solo para administradores
    return render(request, 'admin/dashboard.html')

@admin_or_cashier_required
def manage_orders(request):
    # Para administradores y cajeros
    return render(request, 'orders/manage.html')

@client_required
def my_reservations(request):
    # Solo para clientes
    return render(request, 'reservations/my_reservations.html')

# O usando el decorador genérico:
@role_required('ADMIN', 'CAJERO')
def some_shared_view(request):
    # Para admin y cajeros
    return render(request, 'shared/view.html')
# Create your views here.

@client_required
def perfil_usuario(request):
    return render(request, 'perfil.html', {
        'usuario': request.user
    })
