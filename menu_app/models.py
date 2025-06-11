# Este archivo ahora importa los modelos del módulo models
from .models.category import Category
from .models.product import Product
from .models.rating import Rating
from orders.models import Order, OrderItem

# Exportamos todas las clases para mantener compatibilidad con el código existente
__all__ = ['Category', 'Product', 'Rating', 'Order', 'OrderItem']