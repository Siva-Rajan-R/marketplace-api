from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,ResponseContentTypDict,ORJSONResponse,and_,or_
from app.data_formats.enums.product_enum import ProductCategoryEnum
from app.data_formats.enums.user_enum import RoleEnum
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.products_model import Products
from app.utils.uuid_generator import generate_uuid



class ProductCrud(BaseCrud):
    # This whole class is only for internal use only
    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value,RoleEnum.ADMIN.value])
    async def add(self,name:str,description:str,category:ProductCategoryEnum,barcode:str,product_id:Optional[str]=None):
        # Which is an global product data storing, currently no need for checking anything internal use only
        product_id:str=generate_uuid() if not product_id else product_id
        product_toadd=Products(
            id=product_id,
            name=name,
            description=description,
            category=category.value if isinstance(category,ProductCategoryEnum) else category,
            barcode=barcode
        )

        self.session.add(product_toadd)

        response_content=ResponseContentTypDict(
            status=201,
            succsess=True,
            msg="Product added successfully"
        )

        return ORJSONResponse(
            status_code=201,
            content={"detail":response_content}
        )

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value,RoleEnum.ADMIN.value])
    async def update(self, product_id:str,name:str,description:str,category:ProductCategoryEnum,barcode:str):
        product_toupdate=update(
            Products
        ).where(
            and_(
                Products.id==product_id,
                Products.barcode==barcode
            )
        ).values(
            name=name,
            description=description,
            category=category.value,
        ).returning(Products.id)

        is_updated=(await self.session.execute(product_toupdate))

        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg="Product updated successfully"
        )

        if not is_updated:
            response_content=ResponseContentTypDict(
                status=404,
                succsess=False,
                msg="Error : Updating product",
                description="Product id not found"
            )

            raise HTTPException(status_code=404,detail=response_content)
        
        return ORJSONResponse(content={"detail":response_content},status_code=200)
    

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value,RoleEnum.ADMIN.value])
    async def delete(self,product_id:str,barcode:str):
        product_todel=delete(
            Products
        ).where(
            and_(
                Products.id==product_id,
                Products.barcode==barcode
            )
        ).returning(Products.id)

        is_deleted=(await self.session.execute(product_todel)).scalar_one_or_none()

        response_content=ResponseContentTypDict(
            status=200,
            msg="Product deleted successfully",
            succsess=True
        )

        if not is_deleted:
            response_content=ResponseContentTypDict(
                status=404,
                succsess=False,
                msg="Error : Deleting product",
                description="Product id not found"
            )

            raise HTTPException(status_code=404,detail=response_content)

        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    

    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value,RoleEnum.ADMIN.value,RoleEnum.USER.value])
    async def get(self,query:Optional[str]="",offset:Optional[int]=0,limit:Optional[int]=10):
        formatted_query=f"%{query.lower()}%"
        products_toget=(
            await self.session.execute(
                select(
                    Products.id.label("product_id"),
                    Products.name.label("product_name"),
                    Products.description.label("product_description"),
                    Products.category.label("product_category"),
                    Products.barcode.label("product_barcode")
                ).where(
                    or_(
                        Products.barcode.ilike(formatted_query),
                        Products.name.ilike(formatted_query),
                        Products.description.ilike(formatted_query),
                        Products.category.ilike(formatted_query)
                    )
                    
                ).offset(offset).limit(limit)
            )
        ).mappings().all()

        return {'products':products_toget}
    
    
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value,RoleEnum.ADMIN.value,RoleEnum.USER.value])
    async def get_byid(self,product_barcode_id:str):
        product_toget=(
            await self.session.execute(
                select(
                    Products.id.label("product_id"),
                    Products.name.label("product_name"),
                    Products.description.label("product_description"),
                    Products.category.label("product_category"),
                    Products.barcode.label("product_barcode")
                ).where(
                    or_(
                        Products.id==product_barcode_id,
                        Products.barcode==product_barcode_id
                    )
                    
                )
            )
        ).mappings().one_or_none()

        return {'product':product_toget}
