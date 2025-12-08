from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,or_,and_,ORJSONResponse,ResponseContentTypDict,literal,BackgroundTasks
from app.data_formats.enums.user_enum import RoleEnum
from fastapi.requests import Request
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.register_model import Register
from .account_crud import AccountCrud,Accounts
from .shop_crud import ShopCrud,ShopTypeEnum
from app.database.models.pg_models.shops_model import Shops
from app.utils.uuid_generator import generate_uuid
from app.services.email_service import DebEmailService
from app.database.configs.redis_config import set_redis
from app.utils.email_senders import send_registeration_accept_req_email
from app.security.url_secret_generator import UrlSecretGenerator
from app.configs.webpage_config import TEMPLATE
from dotenv import load_dotenv
import os,orjson
from typing import Annotated
load_dotenv()

@dataclass(frozen=True)
class RegisterCrud(BaseCrud):
    session:AsyncSession

    @catch_errors
    async def verify_email_exists(self,email:EmailStr)->Register:
        register=(await self.session.execute(
            select(
                Register
            ).where(
                and_(
                    Register.email==email
                )
            )
        )).scalar_one_or_none()

        ic(register)
        return register


    @catch_errors
    @start_db_transaction
    async def add(self,name:str,email:EmailStr,mobile_number:str,description:str,shop_type:ShopTypeEnum,bgt:BackgroundTasks):
        ic(email,name,mobile_number,description,shop_type)
        is_exists=await self.verify_email_exists(email=email)
        if is_exists:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    succsess=False,
                    msg="Error : Registeration adding",
                    description="User request already in queued..."
                )
            )
        ic(is_exists)

        account=await AccountCrud(
            session=self.session,
            current_user_role=RoleEnum.SUPER_ADMIN,
            current_user_email="",
            current_user_id="",
            current_user_name=""
        ).verify_account_exists(account_id_email=email)
        ic(account)

        if account:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    succsess=False,
                    msg="Error : Registeration adding",
                    description="User already exists"
                )
            )
        
        registeration_toadd=Register(
            email=email,
            name=name,
            description=description,
            shop_type=shop_type,
            mobile_number=mobile_number
        )

        self.session.add(registeration_toadd)

        # for sending registeration accept email
        bgt.add_task(
            send_registeration_accept_req_email,
            email=email,
            name=name.title(),
            description=description,
            shop_type=shop_type,
            mobile_no=mobile_number    
        )


        return ORJSONResponse(
            status_code=201,
            content={'detail':ResponseContentTypDict(
                status=201,
                succsess=True,
                msg="User registeration successfully, waiting for confirmation"
            )}
        )

    async def update(self):
        """this is just a wrapper for basecrud ABC"""
        ...


    @catch_errors
    @start_db_transaction
    async def transfer(self,email:str)->Register:
        """THis method is used to transfer the data of registerd table data  to accounts table"""
        registered_user=await self.verify_email_exists(email=email)
        if not registered_user:
            return False
        
        await self.session.execute(
            delete(Register).where(Register.email==email)
        )

        await AccountCrud(
            session=self.session,
                current_user_role=RoleEnum.SUPER_ADMIN,
                current_user_email="",
                current_user_id="",
                current_user_name=""
            ).add(
                name=registered_user.name,
                email=registered_user.email,
                role=RoleEnum.SUPER_ADMIN,
                mobile_number=registered_user.mobile_number
        )

        return registered_user
        


    @catch_errors
    @start_db_transaction
    async def delete(self,email:str)->dict:
        is_deleted=(await self.session.execute(delete(Register).where(Register.email==email).returning(Register.email,Register.name,Register.mobile_number,Register.description,Register.shop_type))).mappings().one_or_none()

        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg="Registeration deleted successfully"
        )

        if not is_deleted:
            return False
        
        return is_deleted
    

    async def get(self):
        """this is just a wrapper for basecrud ABC"""
        ...

    async def get_byid(self):
        """this is just a wrapper for basecrud ABC"""
        ...
    

    
