# views/__init__.py
from .home_view import HomeView
from .menu_list_view import MenuListView
from .product_detail_view import ProductDetailView
from .menu_por_categorias import menu_por_categorias
from .order_views import agregar_al_carrito, ver_carrito, confirmar_pedido


__all__ = [
        'HomeView', 
        'MenuListView', 
        'ProductDetailView', 
        'menu_por_categorias',
        'agregar_al_carrito',
        'ver_carrito',
        'confirmar_pedido',
]

