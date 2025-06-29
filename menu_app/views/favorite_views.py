from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from menu_app.models.product import Product
from menu_app.models.favorite import Favorite

@login_required
def add_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('menu_por_categorias')

@login_required
def remove_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.filter(user=request.user, product=product).delete()
    return redirect('menu_por_categorias')