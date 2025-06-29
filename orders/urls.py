from django.urls import path
from .views import AddToCartView, ConfirmarPedidoView, PaymentView, PaymentSuccessView, VerCarritoView, MisPedidosView

app_name = 'orders'

urlpatterns = [
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='agregar_al_carrito'),
    path('carrito/', VerCarritoView.as_view(), name='ver_carrito'),
    path('confirmar/', ConfirmarPedidoView.as_view(), name='confirmar_pedido'),
    path('mis-pedidos/', MisPedidosView.as_view(), name='mis_pedidos'),
    path('payment/<int:order_id>/', PaymentView.as_view(), name='process_payment'),
    path('payment/success/<int:order_id>/', PaymentSuccessView.as_view(), name='payment_success'),
]
