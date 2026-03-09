from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class SeasonalDiscount(DiscountStrategy):
    def __init__(self, percentage: float = 0.10):
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage)

class VIPDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        if total > 500:
            return total - 100
        return total * 0.95