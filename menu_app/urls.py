from django.urls import path
from .views import HomeView, MenuListView, ProductDetailView, MenuPorCategoriasView
from django.contrib import admin
from orders.views import ManejaPedido
from .views.rating import RatingCreateView, RatingUpdateView, RatingDeleteView

urlpatterns = [ 
    path("", HomeView.as_view(), name="home"),
    path("menu/", MenuPorCategoriasView.as_view(), name="menu_por_categorias"),
    path("menu/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('agregar/<int:producto_id>/', ManejaPedido.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ManejaPedido.ver_carrito, name='ver_carrito'),
    path('confirmar/', ManejaPedido.confirmar_pedido, name='confirmar_pedido'),
    path('mis-pedidos/', ManejaPedido.mis_pedidos, name='mis_pedidos'),
    path('calificar/<int:product_id>/', RatingCreateView.as_view(), name='calificar_producto'),
    path('calificacion/<int:pk>/editar/', RatingUpdateView.as_view(), name='editar_calificacion'),
    path('calificacion/<int:pk>/eliminar/', RatingDeleteView.as_view(), name='eliminar_calificacion'),
]