from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,and_,or_,ORJSONResponse,ResponseContentTypDict
from app.data_formats.enums.user_enum import RoleEnum
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.shops import Shops
from app.data_formats.enums.shop_enum import ShopTypeEnum
from app.data_formats.typed_dicts.shop_typdict import ShopAddressTypDict
from app.database.models.pg_models.employees import Employees
from app.database.models.pg_models.accounts import Accounts
from app.utils.uuid_generator import generate_uuid


@dataclass(frozen=True)
class ShopCrud(BaseCrud):
    session:AsyncSession
    current_user_role:RoleEnum
    current_user_id:str


    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def add(self,name:str,description:str,address:ShopAddressTypDict,mobile_number:str,shop_type:ShopTypeEnum,gst_no:Optional[str]=None):
        shop_id:str=generate_uuid()
        shop_toadd=Shops(
            id=shop_id,
            name=name,
            description=description,
            type=shop_type.value,
            gst_no=gst_no,
            account_id=self.current_user_id,
            is_verified=False,
            address=address,
            mobile_number=mobile_number
            
        )
        self.session.add(shop_toadd)

        response_content=ResponseContentTypDict(
            status=201,
            succsess=True,
            msg='Shop created successfully'
        )

        return ORJSONResponse(
            status_code=201,
            content={"detail":response_content}
        )

    
    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def update(self,shop_id:str,name:str,description:str,mobile_number:str,address:ShopAddressTypDict,shop_type:ShopTypeEnum,gst_no:Optional[str]=None):
        shop_toupdate=update(
            Shops
        ).where(
            and_(Shops.id==shop_id,Shops.account_id==self.current_user_id)
        ).values(
            name=name,
            description=description,
            type=shop_type.value,
            gst_no=gst_no,
            address=address,
            mobile_number=mobile_number
        ).returning(Shops.id)

        is_updated=(await self.session.execute(shop_toupdate)).scalar_one_or_none()
        
        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg='Shop data updated successfully'
        )

        if not is_updated:
            response_content=ResponseContentTypDict(
                status=404,
                succsess=False,
                msg="Error : Updaing shop data",
                description="Shop id not found"
            )

            raise HTTPException(
                status_code=404,
                detail=response_content
            )

        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def delete(self,shop_id:str):
        shop_todel=delete(
            Shops
        ).where(
            and_(
                Shops.id==shop_id,
                Shops.account_id==self.current_user_id
            )
        ).returning(Shops.id)

        is_deleted=(await self.session.execute(shop_todel)).scalar_one_or_none()

        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg='Shop deleted successfully'
        )
        if not is_deleted:
            response_content=ResponseContentTypDict(
                status=404,
                succsess=False,
                msg="Error : Deleting shop data",
                description="Shop id not found"
            )

            raise HTTPException(
                status_code=404,
                detail=response_content
            )
        
        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    
    
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get(self):
        shops_toget=(
            await self.session.execute(
                select(
                    Shops.id.label("shop_id"),
                    Shops.name.label("shop_name"),
                    Shops.description.label("shop_description"),
                    Shops.address.label("shop_address"),
                    Shops.gst_no.label("shop_gst_no"),
                    Shops.created_at.label("shop_created_at"),
                    Shops.type.label("shop_type"),
                    Shops.is_verified.label("shop_verified"),
                    Shops.mobile_number.label("shop_mobile_number")
                )
                .where(
                    Shops.account_id==self.current_user_id
                )
            )
        ).mappings().all()

        return {'shops':shops_toget}


    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get_byid(self,shop_id:str):
        shop_toget=(
            await self.session.execute(
                select(
                    Shops.id.label("shop_id"),
                    Shops.name.label("shop_name"),
                    Shops.description.label("shop_description"),
                    Shops.address.label("shop_address"),
                    Shops.gst_no.label("shop_gst_no"),
                    Shops.created_at.label("shop_created_at"),
                    Shops.type.label("shop_type"),
                    Shops.is_verified.label("shop_verified"),
                    Shops.mobile_number.label("shop_mobile_number")
                )
                .where(
                    and_(
                        Shops.account_id==self.current_user_id,
                        Shops.id==shop_id
                     )
                )
            )
        ).mappings().one_or_none()

        return {'shop':shop_toget}
    
    @catch_errors
    async def get_by_account(self,account_id:str):
        owned_q = (
            select(
                Shops.id.label("shop_id"),
                Shops.name.label("shop_name"),
                Shops.description.label("shop_description"),
                Shops.address.label("shop_address"),
                Shops.gst_no.label("shop_gst_no"),
                Shops.created_at.label("shop_created_at"),
                Shops.type.label("shop_type"),
                Shops.is_verified.label("shop_verified"),
                Shops.mobile_number.label("shop_mobile_number")
            )
            .where(Shops.account_id == account_id)
        )

    # Shops where account is an employee
        employee_q = (
            select(
                Shops.id.label("shop_id"),
                Shops.name.label("shop_name"),
                Shops.description.label("shop_description"),
                Shops.address.label("shop_address"),
                Shops.gst_no.label("shop_gst_no"),
                Shops.created_at.label("shop_created_at"),
                Shops.type.label("shop_type"),
                Shops.is_verified.label("shop_verified"),
                Shops.mobile_number.label("shop_mobile_number")
            )
            .join(Employees, Employees.shop_id == Shops.id)
            .where(Employees.account_id == account_id)
        )

        is_owner=(await self.session.execute(select(Shops.id).where(Shops.account_id==account_id).limit(1))).scalar_one_or_none()

        # Combine both using UNION (avoid duplicates)
        final_q = owned_q.union(employee_q)

        result = (await self.session.execute(final_q)).mappings().all()

        if is_owner:
            is_owner=True
        else:
            if result==[]:
                is_owner=True
            else:
                is_owner=False

        return {'shops':result,"is_owner":is_owner}