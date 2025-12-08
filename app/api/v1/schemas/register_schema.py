from pydantic import BaseModel,EmailStr
from app.data_formats.enums.shop_enum import ShopTypeEnum


class RegisterationAddSchema(BaseModel):
    name:str
    email:EmailStr
    mobile_number:str
    description:str
    shop_type:ShopTypeEnum