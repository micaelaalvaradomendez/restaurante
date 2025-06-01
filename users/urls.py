from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil_view, name='perfil'),
    #path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register')
    # otras rutas...
]
