"""
URL configuration for restaurante project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("menu_app.urls")),
    path("bookings/", include("bookings.urls")),
    path("orders/", include("orders.urls")),
    path("users/", include("users.urls")),
    path("notifications/", include("notifications.urls")),
    path('usuario/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('custom-admin/', include('admin_custom.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True
    ), name='login'),    
]
