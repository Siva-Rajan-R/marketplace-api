from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.user_enum import RoleEnum
from app.data_formats.typed_dicts.shop_typdict import ShopAddressTypDict
from app.data_formats.enums.shop_enum import ShopTypeEnum

class AddShopSchema(BaseModel):
    name: str
    description: str
    address:ShopAddressTypDict
    gst_no:Optional[str]
    shop_type:ShopTypeEnum
    mobile_number:str

class UpdateShopSchema(BaseModel):
    name: str
    description: str
    address:ShopAddressTypDict
    gst_no:Optional[str]
    shop_type:ShopTypeEnum
    mobile_number:str