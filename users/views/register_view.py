
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login1')  # o donde quieras redirigir luego de registrar
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
