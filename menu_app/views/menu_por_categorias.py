from django.shortcuts import render
from django.views import View
from menu_app.models.category import Category
from menu_app.models.product import Product
from menu_app.models.favorite import Favorite

class MenuPorCategoriasView(View):
    def get(self, request):
        categorias_con_productos = []

        # Favoritos solo si el usuario está autenticado
        if request.user.is_authenticated:
            favoritos_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
            favoritos = Product.objects.filter(id__in=favoritos_ids)
            if favoritos.exists():
                categorias_con_productos.append(('Favoritos', favoritos))

        # Luego el resto de las categorías
        for categoria in Category.objects.all():
            productos = Product.objects.filter(categories=categoria)
            if productos.exists():
                categorias_con_productos.append((categoria, productos))

        return render(request, "menu/menu_por_categorias.html", {
            "categorias_con_productos": categorias_con_productos,
            "favoritos_ids": list(favoritos_ids) if request.user.is_authenticated else [],
        })
