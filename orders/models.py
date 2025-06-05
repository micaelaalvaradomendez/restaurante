from django.db import models
from django.contrib.auth import get_user_model
from menu_app.models import Product

User = get_user_model()

class Order(models.Model):
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

    def __str__(self):
        return f"{self.quantity}x {self.product.name} en {self.order.code}"