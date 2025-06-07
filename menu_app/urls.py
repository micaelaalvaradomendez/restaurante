from django.urls import path
from .views import HomeView, MenuListView, ProductDetailView, menu_por_categorias, agregar_al_carrito, ver_carrito, confirmar_pedido
from django.contrib import admin

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("menu/", MenuListView.as_view(), name="menu"),
    path("menu/", menu_por_categorias, name="menu_por_categorias"),
    path("menu/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('confirmar/', confirmar_pedido, name='confirmar_pedido'),

]  