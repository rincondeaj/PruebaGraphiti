from domain import Order
from interfaces import InventorySystem, PaymentGateway, NotificationService
from discounts import DiscountStrategy, NoDiscount
from utils import log_execution

class OrderManager:
    def __init__(
        self,
        inventory: InventorySystem,
        payment: PaymentGateway,
        notifier: NotificationService,
        discount_policy: DiscountStrategy = NoDiscount()
    ):
        self.inventory = inventory
        self.payment = payment
        self.notifier = notifier
        self.discount_policy = discount_policy 
        self.processed_count = 0

    @log_execution
    async def process_new_order(self, order: Order) -> str:
        # 1. Nueva validación de seguridad (Cambio estructural)
        if len(order.items) > 100:
            return "FAILED: Fraud Risk - Too many items"

        order.customer.add_audit_entry(f"Processing order {order.order_id}")

        for item in order.items:
            has_stock = await self.inventory.check_stock(item.product_id, item.quantity)
            if not has_stock:
                return "FAILED: Out of Stock"

        # 2. Aplicar descuento y un NUEVO recargo fijo por gestión
        base_price = self.discount_policy.apply(order.total_amount)
        service_fee = 5.99
        final_price = base_price + service_fee

        # 3. Lógica de pago actualizada
        paid = await self.payment.process_payment(final_price)
        if not paid:
            return "FAILED: Payment Declined"

        for item in order.items:
            await self.inventory.reduce_stock(item.product_id, item.quantity)
        
        await self.notifier.send_confirmation(order.customer.email, order.order_id)
        
        self.processed_count += 1
        # El mensaje de éxito ahora es distinto
        return f"SUCCESS: Paid {final_price} (Fee: {service_fee} included)"