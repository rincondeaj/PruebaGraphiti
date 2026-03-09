import asyncio
from domain import Order, Customer, OrderItem
from interfaces import InventorySystem, PaymentGateway, NotificationService
from services import OrderManager
from discounts import VIPDiscount, SeasonalDiscount

class LocalInventory(InventorySystem):
    async def check_stock(self, product_id: str, qty: int) -> bool:
        return True
    async def reduce_stock(self, product_id: str, qty: int) -> None:
        print(f"[DB] Stock reduced for {product_id}")

class StripeAdapter(PaymentGateway):
    async def process_payment(self, amount: float, currency: str = "EUR") -> bool:
        print(f"[STRIPE] Charging {amount} {currency}")
        return True

class PayPalAdapter(PaymentGateway):
    async def process_payment(self, amount: float, currency: str = "USD") -> bool:
        print(f"[PAYPAL] Charging {amount} {currency}")
        return True

class EmailSender(NotificationService):
    async def send_confirmation(self, email: str, order_id: str) -> None:
        print(f"[EMAIL] Sent to {email}")

async def main():
    from factories import PaymentFactory
    
    inventory = LocalInventory()
    
    payment_gw = PaymentFactory.get_payment_gateway("stripe")
    
    notifier = EmailSender()
    
    discount = VIPDiscount()

    manager = OrderManager(inventory, payment_gw, notifier, discount)

    customer = Customer(id="C1", name="Juan", email="juan@test.com", is_vip=True)
    item1 = OrderItem(product_id="P-001", quantity=1, unit_price=600.0)
    
    order = Order(order_id="ORD-X", customer=customer, items=[item1])

    print("--- START ---")
    res = await manager.process_new_order(order)
    print(res)
    
    print(f"Audit Log del Cliente: {customer.last_action}")

if __name__ == "__main__":
    asyncio.run(main())