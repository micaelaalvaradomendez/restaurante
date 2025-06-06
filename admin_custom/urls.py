from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/approve/', views.approve_booking, name='approve_booking'),
    path('bookings/<int:pk>/reject/', views.reject_booking, name='reject_booking'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('tables/', views.TableManagementView.as_view(), name='table_management'),  # <-- Agrega esta línea
]