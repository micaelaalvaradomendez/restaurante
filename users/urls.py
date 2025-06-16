from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', views.register_view, name='register'),
]
