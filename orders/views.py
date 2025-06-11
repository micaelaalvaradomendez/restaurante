
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
        precio = sum(producto.price * carrito.get(str(producto.id), 0) for producto in productos)
        return render(request, 'menu/carrito.html', {'productos': productos, 'carrito': carrito, 'precio': precio})

    def confirmar_pedido(request):
        carrito = request.session.get('carrito', {})
        if not carrito:
            return redirect('menu_por_categorias')
                
        Total =sum(producto.price * cantidad for producto_id, cantidad in carrito.items() if (producto := Product.objects.filter(id=producto_id).first()))
        ultimo_pedido = Order.objects.order_by('-id').first()
        nuevo_id = (ultimo_pedido.id if ultimo_pedido else 0) + 1

        pedido = Order.objects.create(
            user=request.user,
            code=f"PED{nuevo_id:04d}",
            buy_date=timezone.now(),
            state='PREPARACION',
            amount=Total,
        )
        
        for producto_id, cantidad in carrito.items():
            producto = Product.objects.get(id=producto_id)
            OrderItem.objects.create(
                order=pedido, 
                product=producto, 
                quantity=cantidad, 
                price_at_purchase=producto.price
            )

        pedido.confirmado = True
        pedido.save()
        request.session['carrito'] = {}
        return render(request, 'menu/pedido_confirmado.html')

    def mis_pedidos(request):
        pedidos = Order.objects.filter(user=request.user).order_by('-buy_date')
        return render(request, 'menu/mis_pedidos.html', {'pedidos': pedidos})