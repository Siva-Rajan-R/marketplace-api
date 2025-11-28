from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.user_enum import RoleEnum


class AddAccountSchema(BaseModel):
    name:str
    email:EmailStr

class UpdateAccountSchema(BaseModel):
    name:str
    email:EmailStr