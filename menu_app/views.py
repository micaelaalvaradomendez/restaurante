# Este archivo ahora importa las vistas del módulo views
from .views.home_view import HomeView
from .views.menu_list_view import MenuListView
from .views.product_detail_view import ProductDetailView

# Exportamos todas las clases para mantener compatibilidad con el código existente
__all__ = ['HomeView', 'MenuListView', 'ProductDetailView']
