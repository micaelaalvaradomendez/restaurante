# views/__init__.py
from .home_view import HomeView
from .menu_list_view import MenuListView
from .product_detail_view import ProductDetailView
from .menu_por_categorias import menu_por_categorias

__all__ = ['HomeView', 'MenuListView', 'ProductDetailView', 'menu_por_categorias']
