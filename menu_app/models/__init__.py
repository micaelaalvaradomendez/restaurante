# models/__init__.py
from .category import Category
from .product import Product
from .rating import Rating
from .order import Pedido, ItemPedido  # <-- AGREGA ESTA LÍNEA

__all__ = ['Category', 'Product', 'Rating', 'Pedido', 'ItemPedido']
