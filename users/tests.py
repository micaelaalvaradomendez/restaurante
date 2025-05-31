from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.db import IntegrityError

User = get_user_model()

class UserModelTests(TestCase):

    # verifica que el usuario administrador se cree correctamente
    def test_crear_usuario_admin(self):
        user = User.objects.create_user(username='admin_user', email='admin@restaurante.com', password='admin123', rol='ADMIN')
        assert user.rol == 'ADMIN'
        assert user.is_admin() is True
        assert user.can_manage_products() is True
        assert user.can_manage_bookings() is True
        assert user.can_view_reports() is True
        assert user.can_make_reservations() is False

    # verifica que el usuario cajero se cree correctamente
    def test_create_usuario_cajero(self):
        user = User.objects.create_user(username='cajero_user', email='cajero@restaurante.com', password='cajero123', rol='CAJERO')
        assert user.rol == 'CAJERO'
        assert user.is_cashier() is True
        assert user.can_manage_products() is False
        assert user.can_manage_bookings() is True
        assert user.can_view_reports() is False
        assert user.can_make_reservations() is False

    # verifica que el usuario cliente se cree correctamente
    def test_create_usuario_cliente(self):
        user = User.objects.create_user(username='cliente_user', email='cliente@restaurante.com', password='cliente123', rol='CLIENTE')
        assert user.rol == 'CLIENTE'
        assert user.is_client() is True
        assert user.can_manage_products() is False
        assert user.can_manage_bookings() is False
        assert user.can_view_reports() is False
        assert user.can_make_reservations() is True

    # Verifica que el correo electrónico sea único
    def test_email_unico(self):
        User.objects.create_user(username='usuario1', email='correo@restaurante.com', password='test123')
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username='usuario2', email='correo@restaurante.com', password='test456')

    # verifica que el nombre de usuario sea único
    def test_string_representation(self):
        user = User.objects.create_user(username='pedro123', email='pedro@restaurante.com', rol='CAJERO', password='pass123')
        self.assertEqual(str(user), "pedro123 (Cajero)")

 