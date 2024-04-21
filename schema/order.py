from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OrderStatus(str, Enum):
    pending = 'pending'
    processing = 'processing'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'



class PizzaSizes(str, Enum):
    small ='small'
    medium ='medium'
    large = 'large'
    extra_large = 'extra_large'


class OrderModel(BaseModel):
    quantity: int
    pizza_size: Optional[PizzaSizes] = PizzaSizes.small


    class Config:

        json_schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_size": "small",
            }
        }