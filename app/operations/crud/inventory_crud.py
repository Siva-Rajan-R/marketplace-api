from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,ORJSONResponse,ResponseContentTypDict,or_,and_
from app.data_formats.enums.user_enum import RoleEnum
from app.data_formats.enums.product_enum import ProductCategoryEnum
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.inventory_model import Inventory
from app.database.models.pg_models.products_model import Products
from app.operations.crud.shop_crud import ShopCrud
from app.utils.uuid_generator import generate_uuid
from .product_crud import ProductCrud


class InventoryCrud(BaseCrud):

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value])
    # need to check shop id, given barcode is exists
    # check the product exisistence, if not adding it to an product table
    # finally adding to the inventory table for the given shop
    async def add(
        self,
        stocks:int,
        buy_price:float,
        sell_price:float,
        barcode:str,
        cur_user_id:str,
        shop_id:str,
        product_name:str,
        product_description:str,
        product_category:ProductCategoryEnum,
        image_urls:Optional[List[str]]
        
    ):
        product_category=product_category.value #for validation

        is_shop_exists=await ShopCrud(
            session=self.session,
            current_user_role=RoleEnum.SUPER_ADMIN,
            current_user_id=self.current_user_id,
            current_user_name=self.current_user_name,
            current_user_email=self.current_user_email
            ).verify_isexists(shop_id=shop_id)
        
        if not is_shop_exists:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Adding product on inventory",
                    description="Shop doesn't exists"
                )
            )
        
        is_inven_exists=(await self.session.execute(
            select(Inventory.id).where(
                and_(
                    Inventory.barcode==barcode,
                    Inventory.shop_id==shop_id
                )
            )
        )).scalar_one_or_none()

        if is_inven_exists:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    succsess=False,
                    msg="Error : Adding product to inventory",
                    description="Product is already exists"
                )
            )
        
        # checking the barcode has in crt format
        if not barcode or barcode.strip()=="":
            raise HTTPException(
                status_code=422,
                detail=ResponseContentTypDict(
                    status=422,
                    msg="Error : Adding to inventory",
                    succsess=False,
                    description="Invalid barcode format"
                )
            )
        
        # checking the product is exists or not if it hasn't means adding it to an a product table
        product_obj = ProductCrud(session=self.session,current_user_role=self.current_user_role,current_user_email=self.current_user_email,current_user_id=self.current_user_id,current_user_name=self.current_user_name)
        product_info:dict=(await product_obj.get_byid(product_barcode_id=barcode))['product']

        if product_info:
            product_id=product_info['product_id']
            if (
                product_info['product_name'].lower()==product_name.lower() and 
                product_info['product_description'].lower()==product_description.lower() and 
                product_info['product_category'].lower()==product_category.lower()
            ):
                product_name=None
                product_description=None
                product_category=None

        else:
            product_id=generate_uuid()
            await product_obj.add(product_id=product_id,name=product_name,description=product_description,category=product_category,barcode=barcode)
            await self.session.flush()
        

        inventory_id=generate_uuid()
        inventory_toadd=Inventory(
            id=inventory_id,
            product_id=product_id,
            shop_id=shop_id,
            product_name=product_name,
            product_description=product_description,
            product_category=product_category,
            stocks=stocks,
            buy_price=buy_price,
            sell_price=sell_price,
            barcode=barcode,
            image_urls=image_urls,
            added_by=cur_user_id,
        )

        self.session.add(inventory_toadd)
        

        return ORJSONResponse(
            status_code=201,
            content={"detail":ResponseContentTypDict(
                status=201,
                msg="Successfully product added to inventory",
                succsess=True
            )}
        )
    


    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value])
    async def update(
        self,
        inventory_id:str,
        stocks:int,
        buy_price:float,
        sell_price:float,
        barcode:str,
        shop_id:str,
        product_name:str,
        product_description:str,
        product_category:ProductCategoryEnum,
        image_urls:Optional[List[str]],
    ):
        product_category=product_category.value #for validation

        # checking barcode format is valid
        if not barcode or barcode.strip()=="":
            raise HTTPException(
                status_code=422,
                detail=ResponseContentTypDict(
                    status=422,
                    msg="Error : Adding to inventory",
                    succsess=False,
                    description="Invalid barcode format"
                )
            )
        
        # checking the given product is exists on if it means and all the datas should be matched means directly return,
        #  otherwise update that data on the inventory
        product_obj = ProductCrud(session=self.session,current_user_role=self.current_user_role,current_user_email=self.current_user_email,current_user_id=self.current_user_id,current_user_name=self.current_user_name)
        product_info=(await product_obj.get_byid(product_barcode_id=barcode))['product']

        if product_info:
            if (
                product_info['product_name'].lower()==product_name.lower() and 
                product_info['product_description'].lower()==product_description.lower() and 
                product_info['product_category'].lower()==product_category.lower()
            ):

                return ORJSONResponse(
                    status_code=200,
                    content={"detail":ResponseContentTypDict(
                        status=200,
                        msg="Inventory product updated successfully",
                        succsess=True
                    )}
                )

        else:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    succsess=False,
                    msg="Error : Updating inventory product data",
                    description="Productid not found"
                )
            )


        Inventory_toupdate=update(
            Inventory
        ).where(
            and_(
                Inventory.id==inventory_id,
                Inventory.barcode==barcode,
                Inventory.shop_id==shop_id
            )

        ).values(
            product_name=product_name,
            product_description=product_description,
            product_category=product_category,
            stocks=stocks,
            buy_price=buy_price,
            sell_price=sell_price,
            image_urls=image_urls
        ).returning(Inventory.id)


        is_updated=(await self.session.execute(Inventory_toupdate)).scalar_one_or_none()

        if not is_updated:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Updating inventory product data",
                    succsess=False,
                    description="Inventory id not found"
                )
            )
        

        return ORJSONResponse(
            status_code=200,
            content={"detail":ResponseContentTypDict(
                status=200,
                msg="Inventory product updated successfully",
                succsess=True
            )}
        )
    

    
    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value])
    async def delete(self,inventory_id:str,shop_id:str):
        inventory_todel=delete(
            Inventory
        ).where(
            and_(
                Inventory.id==inventory_id,
                Inventory.shop_id==shop_id
            )
        ).returning(Inventory.id)

        is_deleted=(await self.session.execute(inventory_todel)).scalar_one_or_none()

        if not is_deleted:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Deleting inventory product",
                    description="Inventory id not found",
                    succsess=False
                )
            )
        

        return ORJSONResponse(
            status_code=200,
            content={"detail":ResponseContentTypDict(
                status=200,
                msg="Inventory product deleted successfully",
                succsess=True
            )}
        )
    
    
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value])
    async def get(self,shop_id:str,query:Optional[str]="",offset:Optional[int]=0,limit:Optional[int]=10):
        formatted_query=f"%{query}%"
        Inventories_toget=(
            await self.session.execute(
                select(
                    Inventory.id.label("inventory_id"),
                    Inventory.stocks.label("product_stocks"),
                    Inventory.buy_price.label("product_buy_price"),
                    Inventory.sell_price.label("product_sell_price"),
                    Inventory.added_by.label("product_added_by"),
                    Inventory.image_urls.label("product_image_urls"),
                    Inventory.product_id.label("product_id"),
                    Inventory.barcode.label("product_barcode"),
                    Inventory.created_at.label("product_created_at"),
                    func.coalesce(Inventory.product_name, Products.name).label("product_name"),
                    func.coalesce(Inventory.product_description, Products.description).label("product_description"),
                    func.coalesce(Inventory.product_category, Products.category).label("product_category"),
                )
                .join(Products,Products.id==Inventory.product_id)
                .where(Inventory.shop_id==shop_id)
                .where(
                    or_(
                        Inventory.id.ilike(formatted_query),
                        Inventory.shop_id.ilike(formatted_query),
                        Inventory.barcode.ilike(formatted_query),
                        Inventory.added_by.ilike(formatted_query),
                        Inventory.product_name.ilike(formatted_query),
                        Inventory.product_category.ilike(formatted_query),
                        Inventory.product_description.ilike(formatted_query),
                        Products.name.ilike(formatted_query),
                        Products.description.ilike(formatted_query),
                        Products.category.ilike(formatted_query)
                    )
                )
                .offset(offset).limit(limit)
            )
        ).mappings().all()

        return {'inventories':Inventories_toget}
    

    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value])
    async def get_byid(self,shop_id:str,inventory_id:str):
        Inventory_toget=(
            await self.session.execute(
                select(
                    Inventory.id.label("inventory_id"),
                    Inventory.stocks.label("product_stocks"),
                    Inventory.buy_price.label("product_buy_price"),
                    Inventory.sell_price.label("product_sell_price"),
                    Inventory.added_by.label("product_added_by"),
                    Inventory.image_urls.label("product_image_urls"),
                    Inventory.product_id.label("product_id"),
                    Inventory.barcode.label("product_barcode"),
                    Inventory.created_at.label("product_created_at"),
                    func.coalesce(Inventory.product_name, Products.name).label("product_name"),
                    func.coalesce(Inventory.product_description, Products.description).label("product_description"),
                    func.coalesce(Inventory.product_category, Products.category).label("product_category"),
                )
                .join(Products,Products.id==Inventory.product_id)
                .where(and_(
                    Inventory.shop_id==shop_id,
                    Inventory.id==inventory_id
                )
                )
            )
        ).mappings().one_or_none()

        return {'inventory':Inventory_toget}
    



