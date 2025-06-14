from django.shortcuts import render
from django.views import View
from menu_app.models.category import Category
from menu_app.models.product import Product

class MenuPorCategoriasView(View):
    def get(self, request):
        categorias = Category.objects.all()
        categorias_con_productos = []
        for categoria in categorias:
            productos = Product.objects.filter(categories=categoria)
            categorias_con_productos.append((categoria, productos))
        return render(request, "menu/menu_por_categorias.html", {
            "categorias_con_productos": categorias_con_productos
        })
