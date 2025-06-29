import time
import logging

logger = logging.getLogger(__name__)

def process_payment(order, card_details):
    
    logger.info(f"Procesando pago para el pedido {order.code} por un monto de ${order.amount}...")
    time.sleep(1) # Simula la latencia de la red
    logger.info(f"¡Pago para el pedido {order.code} aprobado exitosamente!")
    return True
