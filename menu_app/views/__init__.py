# views/__init__.py
from .home_view import HomeView
from .menu_list_view import MenuListView
from .product_detail_view import ProductDetailView
from .menu_por_categorias import MenuPorCategoriasView
from orders.views import ManejaPedido
from .favorite_views import add_favorite, remove_favorite

__all__ = [
        'HomeView', 
        'MenuListView', 
        'ProductDetailView', 
        'MenuPorCategoriasView',
        'agregar_al_carrito',
        'ver_carrito',
        'confirmar_pedido',
        'mis_pedidos',
        'calificar_producto',
        'ver_calificaciones',
]

