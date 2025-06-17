from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from menu_app.models import Product

User = get_user_model()

class OrderManager(models.Manager):
    def create_order(self, user, products):
        order = self.create(user=user, amount=sum(product.price for product in products))
        for product in products:
            self.model.objects.create(order=order, product=product, quantity=1, price_at_purchase=product.price)
        return order
    
    def crear_pedido_desde_carrito(self, user, carrito):
        # Calcular el total del pedido
        total = sum(
            producto.price * cantidad
            for producto_id, cantidad in carrito.items()
            if (producto := Product.objects.filter(id=producto_id).first())
        )
        
        # Buscar el último pedido para generar un nuevo código
        ultimo_pedido = self.model.objects.order_by('-id').first()
        nuevo_id = (ultimo_pedido.id if ultimo_pedido else 0) + 1

        # Crea el objeto Order
        pedido = self.model.objects.create(
            user=user,
            code=f"PED{nuevo_id:04d}",
            buy_date=timezone.now(),
            state='PREPARACION',
            amount=total,
        )

        # Crear los OrderItems desde el carrito
        for producto_id, cantidad in carrito.items():
            producto = Product.objects.get(id=producto_id)
            OrderItem.objects.create(
                order=pedido,
                product=producto,
                quantity=cantidad,
                price_at_purchase=producto.price
            )

        # Actualizar el stock del producto
        for producto_id, cantidad in carrito.items():
            producto = Product.objects.get(id=producto_id)
            producto.quantity -= cantidad
            if producto.quantity == 0:
                producto.is_available = False
            producto.save() 

        return pedido

class Order(models.Model):
    objects = OrderManager()
    STATES = [
        ('PREPARACION', 'En preparación'),
        ('ENVIADO', 'Enviado'),
        ('RETIRADO', 'Retirado'),
        ('CANCELADO', 'Cancelado'),
    ] 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    buy_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=20, choices=STATES, default='PREPARACION')
    products = models.ManyToManyField(Product, through='OrderItem')

    def __str__(self):
        return f"Pedido #{self.code}"
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.quantity}x {self.product.name} en {self.order.code}"