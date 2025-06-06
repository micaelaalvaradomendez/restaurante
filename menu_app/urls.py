from django.urls import path
from .views import HomeView, MenuListView, ProductDetailView, menu_por_categorias
from django.contrib import admin

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    # path("menu/", MenuListView.as_view(), name="menu"),
    path("menu/", menu_por_categorias, name="menu_por_categorias"),
    path("menu/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),

]  