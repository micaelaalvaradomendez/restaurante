from django.contrib import admin
from django.contrib.auth import get_user_model
from menu_app.models import Product, Category, Rating
from bookings.models import Booking, Table, TimeSlot
from orders.models import Order
from notifications.models import Notification

User = get_user_model()

for model in [User, Product, Category, Booking, Order, Notification, Rating, Table, TimeSlot]:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass

class AdminFilter(admin.SimpleListFilter):
    title = 'Rol de usuario'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return [
            ('ADMIN', 'Administradores'),
            ('CAJERO', 'Cajeros'),
            ('CLIENTE', 'Clientes'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'ADMIN':
            return queryset.filter(rol='ADMIN')
        if self.value() == 'CAJERO':
            return queryset.filter(rol='CAJERO')
        if self.value() == 'CLIENTE':
            return queryset.filter(rol='CLIENTE')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_active')
    list_filter = (AdminFilter, 'is_active')
    search_fields = ('username', 'email')
    readonly_fields = ('last_login', 'date_joined')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available')
    list_filter = ('is_available', 'categories')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)

    def has_change_permission(self, request, obj=None):
        return request.user.rol == 'ADMIN'

    def has_delete_permission(self, request, obj=None):
        return request.user.rol == 'ADMIN'

class BookingAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'table', 'timeslot', 'is_approved', 'is_rejected')
    list_filter = ('is_approved', 'is_rejected', 'timeslot')
    search_fields = ('code', 'user__username')
    actions = ['approve_booking', 'reject_booking']

    def approve_booking(self, request, queryset):
        queryset.update(is_approved=True)
    approve_booking.short_description = "Aprobar reservas seleccionadas"

    def reject_booking(self, request, queryset):
        queryset.update(is_rejected=True)
    reject_booking.short_description = "Rechazar reservas seleccionadas"

    def has_change_permission(self, request, obj=None):
        return request.user.rol in ['ADMIN', 'CAJERO']

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Table)
admin.site.register(TimeSlot)