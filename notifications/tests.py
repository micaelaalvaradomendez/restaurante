from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification, NotificationStatus
from django.utils import timezone

print("Iniciando test del modelo notificaciones...")

User = get_user_model()

class NotificationModelTest(TestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.sender = User.objects.create_user(
            username='maria', 
            email='maria@restaurante.com', 
            password='pass123'
        )
        self.recipient1 = User.objects.create_user(
            username='alberto', 
            email='alberto@gmail.com', 
            password='pass456'
        )
        self.recipient2 = User.objects.create_user(
            username='juliana', 
            email='juliana@gmail.com', 
            password='pass789'
        )
        
        # Crear notificación individual
        self.individual_notification = Notification.objects.create(
            title='Notificación individual',
            message='Este es un mensaje individual',
            sender=self.sender,
            is_global=False
        )
        self.individual_notification.recipients.add(self.recipient1)
        
        # Crear notificación global
        self.global_notification = Notification.objects.create(
            title='Notificación global',
            message='Este es un mensaje para todos',
            sender=self.sender,
            is_global=True
        )

    def test_notification_creation(self):
        # Verifica la creación de una notificación
        notification = Notification.objects.get(id=self.individual_notification.id)
        self.assertEqual(notification.title, 'Notificación individual')
        self.assertEqual(notification.message, 'Este es un mensaje individual')
        self.assertEqual(notification.sender, self.sender)
        self.assertFalse(notification.is_global)
        self.assertIn(self.recipient1, notification.recipients.all())
        self.assertEqual(str(notification), 'Notificación individual')

    def test_global_notification_creation(self):
        # Verifica la creación de una notificación global
        notification = Notification.objects.get(id=self.global_notification.id)
        user_count = User.objects.count()
        self.assertTrue(notification.is_global)
        self.assertEqual(notification.recipients.count(), user_count)  # Todos los usuarios son recipients

    def test_notification_status_creation_for_individual(self):
        # Verifica que se crea el estado de notificación de entrega individual
        statuses = NotificationStatus.objects.filter(notification=self.individual_notification)
        self.assertEqual(statuses.count(), 1)
        self.assertEqual(statuses[0].user, self.recipient1)
        self.assertFalse(statuses[0].is_read)
        
        # Verificar que no se creó para otro destinatario
        with self.assertRaises(NotificationStatus.DoesNotExist):
            NotificationStatus.objects.get(notification=self.individual_notification, user=self.recipient2)

    def test_notification_status_creation_for_global(self):
        # Verifica que se crean estados de notificación para todos los usuarios cuando es global
        statuses = NotificationStatus.objects.filter(notification=self.global_notification)
        user_count = User.objects.count()
        self.assertEqual(statuses.count(), user_count)
        
        # Verificar que se creó para cada usuario
        for user in User.objects.all():
            status = NotificationStatus.objects.get(notification=self.global_notification, user=user)
            self.assertFalse(status.is_read)

    def test_notification_status_unique_together(self):
        # Verifica que no se pueden crear estados duplicados para la misma notificación y usuario
        with self.assertRaises(Exception): 
            NotificationStatus.objects.create(
                notification=self.individual_notification,
                user=self.recipient1,
                is_read=True
            )

    def test_notification_status_ordering(self):
        # Verifica el ordenamiento de los estados de notificación
        another_notification = Notification.objects.create(
            title='Otra notificación',
            message='Mensaje más reciente',
            sender=self.sender,
            is_global=False
        )
        another_notification.recipients.add(self.recipient1)
        
        statuses = NotificationStatus.objects.filter(user=self.recipient1).order_by('-id')
        notifications = [status.notification for status in statuses]
        self.assertIn(another_notification, notifications)
        self.assertIn(self.individual_notification, notifications)

    def test_add_recipient_after_creation(self):
        # Verifica agregar un destinatario después de crear la notificación
        self.individual_notification.recipients.add(self.recipient2)
        statuses = NotificationStatus.objects.filter(notification=self.individual_notification)
        self.assertEqual(statuses.count(), 2)
        
        # Verificar que se creó el nuevo status
        status = NotificationStatus.objects.get(notification=self.individual_notification, user=self.recipient2)
        self.assertFalse(status.is_read)

    def test_notification_status_str(self):
        # Test para el método __str__ de NotificationStatus
        status = NotificationStatus.objects.get(notification=self.individual_notification, user=self.recipient1)
        expected_str = f"{self.recipient1} - {self.individual_notification} - Read: False"
        self.assertEqual(str(status), expected_str)

    def test_mark_as_read(self):
        # Test que verifica marcar una notificación como leída
        status = NotificationStatus.objects.get(notification=self.individual_notification, user=self.recipient1)
        status.is_read = True
        status.save()
        
        updated_status = NotificationStatus.objects.get(notification=self.individual_notification, user=self.recipient1)
        self.assertTrue(updated_status.is_read)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n Finalizaron los tests del modelo notifications.")