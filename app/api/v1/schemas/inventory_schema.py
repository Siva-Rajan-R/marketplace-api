from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.product_enum import ProductCategoryEnum


class AddInventorySchema(BaseModel):
    shop_id:str
    bar_code:str
    stocks:int
    buy_price:float
    sell_price:float
    image_urls:List[str]=[]
    product_id:Optional[str]=None
    product_name:str
    product_description:str
    product_category:ProductCategoryEnum


class UpdateInventorySchema(BaseModel):
    inventory_id:str
    shop_id:str
    bar_code:str
    stocks:int
    buy_price:float
    sell_price:float
    image_urls:List[str]=[]
    product_id:str
    product_name:str
    product_description:str
    product_category:ProductCategoryEnum