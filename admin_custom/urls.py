from django.urls import path
from . import views
from .views import (
    TimeSlotListView, TimeSlotCreateView, TimeSlotUpdateView, TimeSlotDeleteView,
    NotificacionAdminListView, NotificacionAdminCreateView, NotificacionAdminUpdateView, NotificacionAdminDeleteView
)

app_name = 'custom_admin'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/approve/', views.BookingApproveView.as_view(), name='approve_booking'),
    path('bookings/<int:pk>/reject/', views.BookingRejectView.as_view(), name='reject_booking'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update_state/', views.OrderUpdateStateView.as_view(), name='order_update_state'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('tables/', views.TableManagementView.as_view(), name='table_management'), 
    path('tables/add/', views.TableCreateView.as_view(), name='table_add'),
    path('tables/<int:pk>/edit/', views.TableUpdateView.as_view(), name='table_edit'),
    path('tables/<int:pk>/delete/', views.TableDeleteView.as_view(), name='table_delete'),
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot_list'),
    path('timeslots/nuevo/', TimeSlotCreateView.as_view(), name='timeslot_create'),
    path('timeslots/<int:pk>/editar/', TimeSlotUpdateView.as_view(), name='timeslot_update'),
    path('timeslots/<int:pk>/eliminar/', TimeSlotDeleteView.as_view(), name='timeslot_delete'),
    path('notificaciones/', NotificacionAdminListView.as_view(), name='notificaciones_admin'),
    path('notificaciones/nueva/', NotificacionAdminCreateView.as_view(), name='notificaciones_admin_create'),
    path('notificaciones/<int:pk>/editar/', NotificacionAdminUpdateView.as_view(), name='notificaciones_admin_edit'),
    path('notificaciones/<int:pk>/eliminar/', NotificacionAdminDeleteView.as_view(), name='notificaciones_admin_delete'),
]