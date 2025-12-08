from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,or_,and_,ORJSONResponse,ResponseContentTypDict
from app.data_formats.enums.order_enum import OrderOriginEnum,OrderStatusEnum
from app.data_formats.enums.user_enum import RoleEnum
from app.data_formats.typed_dicts.order_typdict import OrderItemTypDict
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.orders_model import Orders
from app.operations.crud.shop_crud import ShopCrud
from app.utils.uuid_generator import generate_uuid


class OrderCrud(BaseCrud):

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value,RoleEnum.USER.value])
    async def add(
        self,
        shop_id:str,
        orders:List[OrderItemTypDict],
        total_price:float,
        order_status:OrderStatusEnum,
        order_origin:OrderOriginEnum,
        customer_number:Optional[str],
        cur_user_id:str
    ):
        # important* Need to implement the inventory related stuffs
        # nedd to check shop id,
        # Then finally add it to orders table
        is_shop_exists=await ShopCrud(
            session=self.session,
            current_user_role=self.current_user_role,
            current_user_id=self.current_user_id,
            current_user_name=self.current_user_name,
            current_user_email=self.current_user_email
        ).verify_isexists(shop_id=shop_id)

        if not is_shop_exists:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Adding product to orders",
                    description="Shop doesn't exists"
                )
            )
        
        order_id=generate_uuid()
        order_toadd=Orders(
            id=order_id,
            shop_id=shop_id,
            orders=orders,
            total_price=total_price,
            status=order_status.value,
            origin=order_origin.value,
            order_by=cur_user_id,
            customer_number=customer_number
        )

        self.session.add(order_toadd)

        return ORJSONResponse(
            status_code=201,
            content={"detail":ResponseContentTypDict(
                status=201,
                msg="Order created successfully",
                succsess=True
            )}
        )
    

    async def update(self):
        """Just a wrapper for ABC , it didn't do anything"""
        pass


    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value,RoleEnum.USER.value])
    @start_db_transaction
    async def update_status(
        self,
        shop_id:str,
        order_id:str,
        order_status:OrderStatusEnum,
        order_origin:OrderOriginEnum,
    ):
        """This method for updating the Order statuses status=>comp,pend,canc, origin=>offline,online"""
        
        ic(order_origin,order_status)
        order_sts_toupdate=update(
            Orders
        ).where(
            Orders.id==order_id,
            Orders.shop_id==shop_id
        ).values(
            status=order_status.value,
            origin=order_origin.value
        ).returning(Orders.id)


        is_sts_updated=(await self.session.execute(order_sts_toupdate)).scalar_one_or_none()

        ic(is_sts_updated)

        if not is_sts_updated:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Updating order status",
                    description="Order id not found",
                    succsess=False
                )
            )
        

        return ORJSONResponse(
            status_code=200,
            content={"detail":ResponseContentTypDict(
                status=200,
                msg="Order status updated successfully",
                succsess=True
            )}
        )
    
    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value,RoleEnum.USER.value])
    async def delete(self,shop_id:str,order_id:str):
        order_todel=delete(
            Orders
        ).where(
            and_(
                Orders.id==order_id,
                Orders.shop_id==shop_id
            )  
        ).returning(Orders.id)


        is_deleted=(await self.session.execute(order_todel)).scalar_one_or_none()


        if not is_deleted:
            raise HTTPException(
                status_code=404,
                detail=ResponseContentTypDict(
                    status=404,
                    msg="Error : Deleting order",
                    description="Order id not found",
                    succsess=False
                )
            )
        

        return ORJSONResponse(
            status_code=200,
            content={"detail":ResponseContentTypDict(
                status=200,
                msg="Order deletedsuccessfully",
                succsess=True
            )}
        )
    
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value,RoleEnum.USER.value])
    async def get(self,shop_id:str,query:Optional[str]="",offset:Optional[int]=0,limit:Optional[int]=10):
        formated_query=f"%{query}%"
        orders_toget=(
            await self.session.execute(
                select(
                    Orders.id.label("order_id"),
                    Orders.orders.label("orders"),
                    Orders.created_at.label("order_created_at"),
                    Orders.customer_number.label("order_customer_number"),
                    Orders.order_by.label("order_by"),
                    Orders.status.label("order_status"),
                    Orders.origin.label("order_origin"),
                    Orders.total_price.label("order_total_price")
                )
                .where(Orders.shop_id==shop_id)
                .where(
                    or_(
                        Orders.customer_number.ilike(formated_query),
                        Orders.origin.ilike(formated_query),
                        Orders.status.ilike(formated_query)
                    )
                )
                .offset(offset).limit(limit)
            )
        ).mappings().all()


        return {'orders':orders_toget}
        
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.ADMIN.value,RoleEnum.SUPER_ADMIN.value,RoleEnum.USER.value])
    async def get_byid(self,shop_id:str,order_id:str):
        order_toget=(
            await self.session.execute(
                select(
                    Orders.id.label("order_id"),
                    Orders.orders.label("orders"),
                    Orders.created_at.label("order_created_at"),
                    Orders.customer_number.label("order_customer_number"),
                    Orders.order_by.label("order_by"),
                    Orders.status.label("order_status"),
                    Orders.origin.label("order_origin"),
                    Orders.total_price.label("order_total_price")
                )
                .where(
                    and_( 
                       Orders.shop_id==shop_id,
                       Orders.id==order_id
                    )
                )
            )
        ).mappings().all()


        return {'order':order_toget}
