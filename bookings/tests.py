from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from bookings.models import TimeSlot, Table, TableTimeSlot, Booking

print("Iniciando test del modelo bookings...")
User = get_user_model()

class BookingModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', email='cliente@gmail.com', password='12345', rol='CLIENTE')

        self.start = timezone.now()
        self.end = self.start + timezone.timedelta(hours=2)
        self.timeslot = TimeSlot.objects.create(start=self.start, end=self.end)

        self.table = Table.objects.create(capacity=4, description='Mesa junto a la ventana')

        self.table_timeslot = TableTimeSlot.objects.create(
            table=self.table,
            timeslot=self.timeslot,
            is_reserved=False
        )

    def test_crear_horario(self):
        self.assertEqual(str(self.timeslot), f"{self.start} - {self.end}")

    def test_crear_mesa(self):
        self.assertEqual(str(self.table), f"Mesa #{self.table.id} (Capacidad: {self.table.capacity})")

    def test_crear_horario_mesa(self):
        self.assertEqual(str(self.table_timeslot), f"Mesa {self.table.id} - {self.timeslot} - Reservada: {self.table_timeslot.is_reserved}")

    def test_create_reserva(self):
        booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            timeslot=self.timeslot,
            code="ABC123",
            is_approved=True,
            approved_date=timezone.now().date(),
            observations="Sin observaciones"
        )
        self.assertEqual(str(booking), f"Reserva #ABC123 - {self.user.username}")
        self.assertTrue(booking.is_approved)
        self.assertEqual(booking.table, self.table)
        self.assertEqual(booking.timeslot, self.timeslot)

    # Verifica que el código de reserva sea único
    def test_codigo_reserva_unico(self):
        Booking.objects.create(
            user=self.user,
            table=self.table,
            timeslot=self.timeslot,
            code="DUPL123"
        )
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                table=self.table,
                timeslot=self.timeslot,
                code="DUPL123"  # Mismo código -> debe fallar por unique=True
            )

    # verifica que no se pueda crear una reserva con un horario ya reservado
    def test_horario_mesa_unico(self):
        with self.assertRaises(Exception):
            TableTimeSlot.objects.create(
                table=self.table,
                timeslot=self.timeslot,
                is_reserved=False
            )

    # Verifica que no se pueda crear una reserva duplicada para la misma mesa y horario
    def test_no_reserva_duplicada_misma_mesa_horario(self):
        Booking.objects.create(
            user=self.user,
            table=self.table,
            timeslot=self.timeslot,
            code="UNICO1"
        )
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                table=self.table,
                timeslot=self.timeslot,
                code="UNICO2"
            )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n Finalizaron los tests del modelo bookings.")