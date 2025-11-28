from .import List,Optional,BaseModel,EmailStr
from app.data_formats.enums.product_enum import ProductCategoryEnum


class AddProductSchema(BaseModel):
    name: str
    description: Optional[str]
    category: ProductCategoryEnum
    barcode: str

class UpdateProductSchema(BaseModel):
    product_id:str
    name: str
    description: Optional[str]
    category: ProductCategoryEnum
    barcode: str

