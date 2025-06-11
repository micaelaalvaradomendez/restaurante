# Este archivo ahora importa las vistas del módulo views
from .views.home_view import HomeView
from .views.menu_list_view import MenuListView
from .views.product_detail_view import ProductDetailView
from orders import agregar_al_carrito, ver_carrito, confirmar_pedido

# from .views.menu_por_categorias import menu_por_categorias

__all__ = ['HomeView', 'MenuListView', 'ProductDetailView', 'agregar_al_carrito', 'ver_carrito', 'confirmar_pedido'] 
