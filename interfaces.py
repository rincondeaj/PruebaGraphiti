from abc import ABC, abstractmethod
from domain import Order

class InventorySystem(ABC):
    @abstractmethod
    async def check_stock(self, product_id: str, qty: int) -> bool:
        """Verifica si hay stock suficiente"""
        pass

    @abstractmethod
    async def reduce_stock(self, product_id: str, qty: int) -> None:
        """Reduce el stock real"""
        pass

class PaymentGateway(ABC):
    @abstractmethod
    async def process_payment(self, amount: float, currency: str = "EUR") -> bool:
        """Procesa el cobro"""
        pass

class NotificationService(ABC):
    @abstractmethod
    async def send_confirmation(self, email: str, order_id: str) -> None:
        pass