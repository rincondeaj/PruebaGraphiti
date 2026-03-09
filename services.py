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

        order.customer.add_audit_entry(f"Processing order {order.order_id}")

        for item in order.items:
            has_stock = await self.inventory.check_stock(item.product_id, item.quantity)
            if not has_stock:
                return "FAILED: Out of Stock"

        final_price = self.discount_policy.apply(order.total_amount)

        paid = await self.payment.process_payment(final_price)
        if not paid:
            return "FAILED: Payment Declined"

        for item in order.items:
            await self.inventory.reduce_stock(item.product_id, item.quantity)
        
        await self.notifier.send_confirmation(order.customer.email, order.order_id)
        
        self.processed_count += 1
        return f"SUCCESS: Paid {final_price}"