from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu_app.models import Product, Pedido, ItemPedido

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    return redirect('menu_por_categorias')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = Product.objects.filter(id__in=carrito.keys())
    return render(request, 'carrito.html', {'productos': productos, 'carrito': carrito})

@login_required
def confirmar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('menu_por_categorias')
    pedido = Pedido.objects.create(usuario=request.user)
    for producto_id, cantidad in carrito.items():
        producto = Product.objects.get(id=producto_id)
        ItemPedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad)
    pedido.confirmado = True
    pedido.save()
    request.session['carrito'] = {}
    return render(request, 'pedido_confirmado.html')