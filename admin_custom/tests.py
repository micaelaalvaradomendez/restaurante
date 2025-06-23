from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.views import View
from .mixins import AdminRequiredMixin, StaffRequiredMixin
from django.urls import reverse
from orders.models import Order

print("Inciando test de custom admin")

User = get_user_model()

class DummyAdminView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return "OK"

class DummyStaffView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return "OK"

class AdminCustomMixinsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User.objects.create_user(username='admin', password='admin', rol='ADMIN')
        self.cajero = User.objects.create_user(username='cajero', password='cajero', rol='CAJERO')
        self.cliente = User.objects.create_user(username='cliente', password='cliente', rol='CLIENTE')

    def test_admin_required_mixin_allows_admin(self):
        request = self.factory.get('/')
        request.user = self.admin
        response = DummyAdminView.as_view()(request)
        self.assertEqual(response, "OK")

    def test_admin_required_mixin_denies_non_admin(self):
        request = self.factory.get('/')
        request.user = self.cajero
        with self.assertRaises(PermissionDenied):
            DummyAdminView.as_view()(request)

    def test_staff_required_mixin_allows_admin(self):
        request = self.factory.get('/')
        request.user = self.admin
        response = DummyStaffView.as_view()(request)
        self.assertEqual(response, "OK")

    def test_staff_required_mixin_allows_cajero(self):
        request = self.factory.get('/')
        request.user = self.cajero
        response = DummyStaffView.as_view()(request)
        self.assertEqual(response, "OK")

    def test_staff_required_mixin_denies_cliente(self):
        request = self.factory.get('/')
        request.user = self.cliente
        with self.assertRaises(PermissionDenied):
            DummyStaffView.as_view()(request)

class CustomAdminTemplatesTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='admin', rol='ADMIN')
        self.client.login(username='admin', password='admin')
        self.order = Order.objects.create(user=self.admin, code='PED-0001', amount=100, state='PREPARACION')

    def test_order_list_template_used(self):
        response = self.client.get(reverse('custom_admin:order_list'))
        self.assertTemplateUsed(response, 'custom_admin/order_list.html')
        self.assertContains(response, 'Pedidos')
        self.assertContains(response, self.order.code)

    def test_order_detail_template_used(self):
        response = self.client.get(reverse('custom_admin:order_detail', args=[self.order.id]))
        self.assertTemplateUsed(response, 'custom_admin/order_detail.html')
        self.assertContains(response, self.order.code)
        self.assertContains(response, 'Total del pedido')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n Finalizaron los tests del custom admin")
