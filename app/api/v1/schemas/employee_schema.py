from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.user_enum import RoleEnum


class AddEmployeeSchema(BaseModel):
    name:str
    email:EmailStr
    role:RoleEnum
    shop_id:str

class UpdateEmployeeSchema(BaseModel):
    employee_id:str
    account_id:str
    role:RoleEnum
    shop_id:str