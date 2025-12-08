from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,ResponseContentTypDict,ORJSONResponse,or_,and_,case
from app.data_formats.enums.user_enum import RoleEnum
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.accounts_model import Accounts
from app.database.models.pg_models.employees_model import Employees
from app.database.models.pg_models.shops_model import Shops
from app.utils.uuid_generator import generate_uuid


@dataclass(frozen=True)
class AccountCrud(BaseCrud):
    session:AsyncSession
    current_user_role:RoleEnum
    current_user_id:str
    current_user_name:str
    current_user_email:EmailStr

    @catch_errors
    async def verify_account_exists(
        self,
        account_id_email: str,
        shop_id: Optional[str | None] = None
    ):
        
        account=(await self.session.execute(select(
            Accounts.id,
            Accounts.email,
            Accounts.role.label("role"),
            Accounts.name
        ).where(
            or_(
                Accounts.id == account_id_email,
                Accounts.email == account_id_email
            )
        ))).mappings().one_or_none()
        account=dict(account) if account else account
        ic(account,type(account))
        if not account:
            return account
        
        if account and shop_id:
            employee=(await self.session.execute(select(Employees.id).where(Employees.account_id==account['id'],Employees.is_accepted==True).limit(1))).mappings().one_or_none()
            if employee:
                role=(await self.session.execute(select(Employees.role).where(Employees.account_id==account['id'],Employees.shop_id==shop_id,Employees.is_accepted==True))).scalar_one_or_none()
                if not role:
                    return None
                account['role']=role
        ic(account)
        return account

    

    @catch_errors
    @start_db_transaction
    async def add(self,name:str,email:EmailStr,role:RoleEnum,mobile_number:str):
        # 1. need to check account exists || 2. need to check the account id exists on employee
        # 3. then add the account to the table
        if await self.verify_account_exists(account_id_email=email):
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    msg="Error : Adding user",
                    description="User already exists",
                    succsess=False
                )
            )
        
        is_exists_emply_tbl=(await self.session.execute(select(Employees.id).where(Employees.account_id==self.current_user_id).limit(1))).scalar_one_or_none()
        if is_exists_emply_tbl:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    succsess=False,
                    msg="Error : Adding employee",
                    description="User already registered as employee"
                )
            )
        
        account_id:str=generate_uuid()
        account_toadd=Accounts(
            id=account_id,
            name=name,
            email=email,
            role=role.value,
            mobile_number=mobile_number
        )

        self.session.add(account_toadd)

        response_content=ResponseContentTypDict(
            status=201,
            msg="Account created successfully",
            succsess=True
        )

        return ORJSONResponse(
            status_code=201,
            content={"detail":response_content}
        )


    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def update(self,account_id:str,name:str,email:EmailStr,role:RoleEnum,mobile_number:str):
        account_toupdate=update(
            Accounts
        ).where(
            Accounts.id==account_id,
        ).values(
            name=name,
            email=email,
            role=role,
            mobile_number=mobile_number
        ).returning(Accounts.id)
        
        is_updated=(await self.session.execute(account_toupdate)).scalar_one_or_none()
        ic(is_updated)
        response_content=ResponseContentTypDict(
            status=200,
            msg="Account updated successfully",
            succsess=True
        )

        if not is_updated:
            response_content=ResponseContentTypDict(
                status=404,
                msg="Error : Updating Account data",
                succsess=False,
                description="Account id not found"
            )

            raise HTTPException(status_code=404,detail=response_content)
        
        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def delete(self,account_id:str):
        Account_todel=delete(
            Accounts
        ).where(
            and_(
                Accounts.id==account_id
            )
        ).returning(Accounts.id)


        is_deleted=(await self.session.execute(Account_todel)).scalar_one_or_none()

        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg="Account deleted successfully"
        )

        if not is_deleted:
            response_content=ResponseContentTypDict(
                status=404,
                msg="Error : Deleting Account data",
                description="Account id not found",
                succsess=False
            )

            raise HTTPException(status_code=404,detail=response_content)
        
        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    
    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get(self,query:Optional[str]="",offset:Optional[int]=0,limit:Optional[int]=10):
        formatted_query:str=f"%{query.lower()}%"
        accounts_toget=(
            await self.session.execute(
                select(
                    Accounts.id.label("account_id"),
                    Accounts.name.label('account_name'),
                    Accounts.email.label("account_email"),
                    Accounts.role.label("account_role")
                )
                .where(
                    or_(
                        Accounts.name.ilike(formatted_query),
                        Accounts.email.ilike(formatted_query),
                        Accounts.role.ilike(formatted_query)
                    )
                )
                .offset(offset).limit(limit)
            )
        ).mappings().all()

        return {'accounts':accounts_toget}
    

    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get_byid(self,account_id:str):
        account_toget=(
            await self.session.execute(
                select(
                    Accounts.id.label("account_id"),
                    Accounts.name.label('account_name'),
                    Accounts.email.label("account_email"),
                    Accounts.role.label("account_role")
                )
                .where(
                    and_(
                        Accounts.id==account_id,
                    )
                )
            )
        ).mappings().one_or_none()

        return {'account':account_toget}
    

    @catch_errors
    async def get_role(self,account_id:str,shop_id:str):
        employee_role=(await self.session.execute(
            select(Employees.role)
            .where(
                and_(
                    Employees.account_id==account_id,
                    Employees.shop_id==shop_id,
                    Employees.is_accepted==True
                ) 
            )
        )).scalar_one_or_none()

        if employee_role:
            return employee_role
        
        owner=(
            await self.session.execute(
                select(
                    Shops.id
                )
                .where(
                    Shops.id==shop_id,
                    Shops.account_id==account_id
                )
            )
        ).scalar_one_or_none()

        if owner:
            return RoleEnum.SUPER_ADMIN.value

        raise HTTPException(
            status_code=404,
            detail=ResponseContentTypDict(
                status=404,
                msg="Error : Unauthorized",
                description="Invalid user or shop id"
            )
        )