from datetime import datetime
from typing import Annotated, List
from pydantic import BaseModel, Field, computed_field, AfterValidator, PrivateAttr

from utils import AuditMixin

def validate_positive(v: float) -> float:
    if v <= 0: raise ValueError("Must be positive")
    return v

Money = Annotated[float, AfterValidator(validate_positive)]

class Customer(BaseModel, AuditMixin):
    id: str
    name: str
    email: str
    is_vip: bool = Field(default=False)
    
    _audit_log: list[str] = PrivateAttr(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)
        AuditMixin.__init__(self)

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    unit_price: Money

class Order(BaseModel):
    order_id: str
    customer: Customer
    items: List[OrderItem]
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "PENDING"

    @computed_field
    def total_amount(self) -> float:
        return sum(item.quantity * item.unit_price for item in self.items)