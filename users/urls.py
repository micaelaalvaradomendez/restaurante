from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),
    path('login1/', views.login1_view, name='login1'),
    path('register/', views.register_view, name='register')
    # otras rutas...
]
