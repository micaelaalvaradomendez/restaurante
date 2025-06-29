from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from menu_app.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class ManejaPedido(LoginRequiredMixin):
    def agregar_al_carrito(request, producto_id):
        producto = get_object_or_404(Product, id=producto_id)
        if not producto.is_available:
            return redirect('menu_por_categorias')
        carrito = request.session.get('carrito', {})
        carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
        producto.price = producto.price
        request.session['carrito'] = carrito
        return redirect('menu_por_categorias')

    def ver_carrito(request):
        carrito = request.session.get('carrito', {})
        productos = Product.objects.filter(id__in=carrito.keys())
        items = []
        for producto in productos:
            cantidad = carrito.get(str(producto.id), 0)
            item = type('Item', (), {})()
            item.product = producto
            item.quantity = cantidad
            item.subtotal = producto.price * cantidad
            items.append(item)
        total = sum(item.subtotal for item in items)
        return render(request, 'menu/carrito.html', {'items': items, 'total': total})

    def confirmar_pedido(request):
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('menu_por_categorias')
                
        pedido = Order.objects.crear_pedido_desde_carrito(request.user, carrito)

        pedido.confirmado = True
        pedido.save()
        request.session['carrito'] = {}
        return render(request, 'menu/pedido_confirmado.html')

    def mis_pedidos(request):
        pedidos = Order.objects.filter(user=request.user).order_by('-buy_date')
        return render(request, 'menu/mis_pedidos.html', {'pedidos': pedidos})