from typing import TypedDict


class OrderItemTypDict(TypedDict):
    product_name:str
    quantity:int
    price:int