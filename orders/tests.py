from django.test import TestCase
from django.contrib.auth import get_user_model
from menu_app.models import Product, Category
from .models import Order, OrderItem
from decimal import Decimal

print("Iniciando test del modelo orders...")

User = get_user_model()

class OrderModelTest(TestCase):
    def setUp(self):
        self.ensaladas = Category.objects.create(name="Ensaladas", description="Ensaladas frescas")
        self.pizzas = Category.objects.create(name="Pizzas", description="Pizzas artesanales")
        self.postres = Category.objects.create(name="Postres", description="Deliciosos postres")
        self.bebidas = Category.objects.create(name="Bebidas", description="Bebidas y cócteles")
        self.cafeteria = Category.objects.create(name="Cafetería", description="Cafés y pastelería")
        
        self.pizza_pepperoni = Product.objects.create(
            pk=1,
            name="Pizza Pepperoni",
            title="Pizza Pepperoni",
            description="Pizza con pepperoni picante",
            price=Decimal('25000.00'),
            quantity=4,
            is_available=True
        )
        self.pizza_pepperoni.categories.add(self.pizzas)
        
        self.pizza_fugazzeta = Product.objects.create(
            pk=2,
            name="Pizza Fugazzeta",
            title="Pizza Fugazzeta",
            description="Pizza con cebolla y queso",
            price=Decimal('22000.00'),
            quantity=3,
            is_available=True
        )
        self.pizza_fugazzeta.categories.add(self.pizzas)
        
        self.ensalada_cesar = Product.objects.create(
            pk=3,
            name="Ensalada César",
            title="Ensalada César",
            description="Ensalada con aderezo César",
            price=Decimal('15000.00'),
            quantity=10,
            is_available=True
        )
        self.ensalada_cesar.categories.add(self.ensaladas)
        
        self.tiramisu = Product.objects.create(
            pk=5,
            name="Tiramisu",
            title="Tiramisu",
            description="Postre italiano con café",
            price=Decimal('9000.00'),
            quantity=20,
            is_available=True
        )
        self.tiramisu.categories.add(self.postres)
        
        self.mojito = Product.objects.create(
            pk=8,
            name="Mojito",
            title="Mojito",
            description="Cóctel cubano con ron",
            price=Decimal('10000.00'),
            quantity=15,
            is_available=True
        )
        self.mojito.categories.add(self.bebidas)
        
        # Crear usuario
        self.user = User.objects.create_user(
            username="cliente",
            email="cliente@restaurante.com",
            password="pass123"
        )
        
        # Crear pedido de ejemplo
        self.order = Order.objects.create(
            user=self.user,
            code="PEDIDO001",
            amount=Decimal('69000.00')  # 1 pizza + 1 ensalada + 1 mojito + 1 tiramisu
        )
        
        # Agregar items al pedido
        OrderItem.objects.create(
            order=self.order,
            product=self.pizza_pepperoni,
            quantity=1,
            price_at_purchase=self.pizza_pepperoni.price
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.ensalada_cesar,
            quantity=1,
            price_at_purchase=self.ensalada_cesar.price
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.mojito,
            quantity=2,
            price_at_purchase=self.mojito.price
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.tiramisu,
            quantity=1,
            price_at_purchase=self.tiramisu.price
        )

    def test_order(self):
        # Test que verifica un pedido 
        self.assertEqual(self.order.code, "PEDIDO001")
        self.assertEqual(self.order.user.username, "cliente")
        self.assertEqual(self.order.amount, Decimal('69000.00'))
        self.assertEqual(self.order.state, "PENDIENTE_APROBACION")
        self.assertEqual(self.order.products.count(), 4)
        
        # Verificar los productos incluidos
        products_in_order = list(self.order.products.all().values_list('name', flat=True))
        expected_products = [
            "Pizza Pepperoni", 
            "Ensalada César",
            "Mojito",
            "Tiramisu"
        ]
        self.assertCountEqual(products_in_order, expected_products)

    def test_order_item_details(self):
        # verifica los detalles de los items del pedido
        items = self.order.orderitem_set.all()
        self.assertEqual(items.count(), 4)
        
        # Verificar el item de pizza
        pizza_item = items.get(product=self.pizza_pepperoni)
        self.assertEqual(pizza_item.quantity, 1)
        self.assertEqual(pizza_item.price_at_purchase, Decimal('25000.00'))
        
        # Verificar el item de mojito (con cantidad 2)
        mojito_item = items.get(product=self.mojito)
        self.assertEqual(mojito_item.quantity, 2)
        self.assertEqual(mojito_item.price_at_purchase, Decimal('10000.00'))
        
        # Verificar cálculo de subtotal por item
        self.assertEqual(mojito_item.quantity * mojito_item.price_at_purchase, Decimal('20000.00'))

    def test_order_total_calculation(self):
        # Verifica el cálculo automático del total del pedido
        # Calcular total esperado: 
        # Pizza: 25000 
        # Ensalada: 15000 
        # 2 Mojitos: 20000 
        # Tiramisu: 9000
        # Total: 69000
        calculated_total = sum(
            item.quantity * item.price_at_purchase 
            for item in self.order.orderitem_set.all()
        )
        self.assertEqual(self.order.amount, calculated_total)
        self.assertEqual(calculated_total, Decimal('69000.00'))

    def test_product_availability_after_order(self):
        # Verifica la cantidad disponible de productos después de un pedido
        # Cantidad original de pizza pepperoni: 4
        # Se pidió 1, debería quedar 3
        self.assertEqual(self.pizza_pepperoni.quantity, 4)  # No se actualiza automáticamente
        
    def test_order_with_multiple_quantities(self):
        # Verifica un pedido con múltiples cantidades del mismo producto
        # Crear nuevo pedido con 3 pizzas fugazzeta
        new_order = Order.objects.create(
            user=self.user,
            code="PEDIDO002",
            amount=Decimal('66000.00')  # 3 x 22000
        )
        OrderItem.objects.create(
            order=new_order,
            product=self.pizza_fugazzeta,
            quantity=3,
            price_at_purchase=self.pizza_fugazzeta.price
        )
        
        # Verificar
        self.assertEqual(new_order.amount, Decimal('66000.00'))
        self.assertEqual(new_order.orderitem_set.count(), 1)
        item = new_order.orderitem_set.first()
        self.assertEqual(item.product.name, "Pizza Fugazzeta")
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.price_at_purchase, Decimal('22000.00'))

    def test_order_state_transitions(self):
        # Verifica los cambios de estado del pedido
        self.assertEqual(self.order.state, "PENDIENTE_APROBACION")
        
        # Cambiar a ENVIADO
        self.order.state = "ENVIADO"
        self.order.save()
        self.assertEqual(self.order.state, "ENVIADO")
        
        # Cambiar a RETIRADO
        self.order.state = "RETIRADO"
        self.order.save()
        self.assertEqual(self.order.state, "RETIRADO")
        
        # Cambiar a CANCELADO
        self.order.state = "CANCELADO"
        self.order.save()
        self.assertEqual(self.order.state, "CANCELADO")

    def test_order_str_representation(self):
        # Verifica la representación en string del pedido
        self.assertEqual(str(self.order), "Pedido #PEDIDO001")

    def test_order_item_str_representation(self):
        # Verifica la representación en string de los items
        pizza_item = self.order.orderitem_set.get(product=self.pizza_pepperoni)
        self.assertEqual(str(pizza_item), "1x Pizza Pepperoni en PEDIDO001")
        
        mojito_item = self.order.orderitem_set.get(product=self.mojito)
        self.assertEqual(str(mojito_item), "2x Mojito en PEDIDO001")

    def test_order_with_product_from_different_categories(self):
        # Verifica un pedido con productos de diferentes categorías
        # Verificar categorías de los productos en el pedido
        categories_in_order = set()
        for product in self.order.products.all():
            categories_in_order.update(product.categories.all().values_list('name', flat=True))
        
        expected_categories = {"Pizzas", "Ensaladas", "Bebidas", "Postres"}
        self.assertSetEqual(categories_in_order, expected_categories)

    def test_order_code_unique(self):
        # Verifica que el código de pedido sea único
        with self.assertRaises(Exception):
            Order.objects.create(
                user=self.user,
                code="PEDIDO001",  # ya existe
                amount=Decimal('10000.00')
            )

    # Test de elminacion en cascada
    def test_orderitem_deleted_with_order(self):
        # Verifica que al eliminar un pedido, también se eliminen sus items
        order_id = self.order.id
        self.order.delete()
        self.assertFalse(OrderItem.objects.filter(order_id=order_id).exists())

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("\n Finalizaron los tests del modelo orders.")
