# Este archivo ahora importa los modelos del módulo models
from .models.category import Category
from .models.product import Product
from .models.rating import Rating
from .models.order import Pedido, ItemPedido

# Exportamos todas las clases para mantener compatibilidad con el código existente
__all__ = ['Category', 'Product', 'Rating', 'Pedido', 'ItemPedido']