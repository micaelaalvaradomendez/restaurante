from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def admin_or_cashier_check(user):
    return user.is_superuser or user.groups.filter(name='Cajeros').exists()

@user_passes_test(admin_or_cashier_check)
def admin_dashboard(request):
    return render(request, 'admin_custom/dashboard.html')
