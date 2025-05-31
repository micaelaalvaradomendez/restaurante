from django.shortcuts import render
from menu_app.models.category import Category
from menu_app.models.product import Product

def menu_por_categorias(request):
    """categorias = Category.objects.all()
    categorias_con_productos = []
    for categoria in categorias:
        productos = Product.objects.filter(categories=categoria)
        categorias_con_productos.append((categoria, productos))
    print("DEBUG:", categorias_con_productos)  # <-- Esto debe mostrar datos en la consola
    return render(request, "menu_por_categorias.html", {
        "categorias_con_productos": categorias_con_productos """
    return render(request, "menu/menu_por_categorias.html", {})
    #})
