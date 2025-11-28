from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.order_enum import OrderStatusEnum, OrderOriginEnum
from app.data_formats.typed_dicts.order_typdict import OrderItemTypDict


class AddOrderSchema(BaseModel):
    shop_id:str
    orders: List[OrderItemTypDict]
    order_total_price: float
    customer_number: Optional[str]
    order_status: OrderStatusEnum
    order_origin: OrderOriginEnum

class UpdateOrderSchema(BaseModel):
    shop_id:str
    order_id:str
    orders: List[OrderItemTypDict]
    order_total_price: float
    customer_number: Optional[str]
    order_status: OrderStatusEnum
    order_origin: OrderOriginEnum


class UpdateOrderStatus(BaseModel):
    shop_id:str
    order_id:str
    order_status:OrderStatusEnum
    order_origin:OrderOriginEnum