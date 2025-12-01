from ..import HTTPException,ic,List,Optional,EmailStr,AsyncSession,dataclass,select,update,delete,insert,func,BaseCrud,or_,and_,ORJSONResponse,ResponseContentTypDict,literal
from app.data_formats.enums.user_enum import RoleEnum
from app.decoraters.auth_decorators import verify_role
from app.decoraters.crud_decoraters import start_db_transaction,catch_errors
from app.database.models.pg_models.employees import Employees
from .account_crud import AccountCrud,Accounts
from app.database.models.pg_models.shops import Shops
from app.utils.uuid_generator import generate_uuid

@dataclass(frozen=True)
class EmployeeCrud(BaseCrud):
    session:AsyncSession
    current_user_role:RoleEnum
    current_user_id:str

    @catch_errors
    async def verify_employee_exists(self,account_id:str,shop_id:str):
        employee=(await self.session.execute(
            select(
                Employees.id,
                Employees.shop_id,
                Employees.account_id
            ).where(
                and_(
                    Employees.account_id==account_id,
                    Employees.shop_id==shop_id
                )
            )
        )).mappings().one_or_none()

        ic(employee)
        return employee


    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def add(self,shop_id:str,name:str,email:EmailStr,role:RoleEnum):
        
        tabeles_toadd=[]
        account_id=None
        account=await AccountCrud(session=self.session,current_user_role=RoleEnum.SUPER_ADMIN).verify_account_exists(account_id_email=email)
        ic(account)
        if not account:
            account_id=generate_uuid()
            account_toadd=Accounts(
                id=account_id,
                name=name,
                email=email,
                role=role
            )

            tabeles_toadd.append(account_toadd)
        else:
            account_id=account['id']
            ic("hello")
            if await self.verify_employee_exists(account_id=account_id,shop_id=shop_id):
                raise HTTPException(
                    status_code=409,
                    detail=ResponseContentTypDict(
                        status=409,
                        msg="Error : Creating employee",
                        description="Employee already exists"
                    )
                )

            
        employee_id:str=generate_uuid()
        employee_toadd=Employees(
            id=employee_id,
            account_id=account_id,
            added_by=self.current_user_id,
            shop_id=shop_id,
            role=role.value
        )

        tabeles_toadd.append(employee_toadd)

        self.session.add_all(tabeles_toadd)

        response_content=ResponseContentTypDict(
            status=201,
            msg="Employee created successfully, Waiting for confirmation",
            succsess=True
        )

        return ORJSONResponse(
            status_code=201,
            content={"detail":response_content}
        )

    async def update(self):
        """this is just a wrapper for basecrud ABC"""
        ...


    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def update_role(self,account_id:str,shop_id:str,employee_id:str,role:RoleEnum):
        employee_toupdate=update(
            Employees
        ).where(
            and_(
                Employees.id==employee_id,
                Employees.shop_id==shop_id,
                Employees.account_id==account_id,
                Employees.added_by==self.current_user_id
            )
        ).values(
            role=role
        ).returning(Employees.id)

        is_updated=(await self.session.execute(employee_toupdate)).scalar_one_or_none()

        
        
        response_content={
            "detail":ResponseContentTypDict(
                status=200,
                msg="Employee role updated successfully",
                succsess=True
            )
        }

        if not is_updated:
            response_content=ResponseContentTypDict(
                status=404,
                msg="Error : Updating employee role",
                succsess=False,
                description="Employee id not found"
            )

            raise HTTPException(status_code=404,detail=response_content)
        
        return ORJSONResponse(
            status_code=200,
            content=response_content
        )
    

    @catch_errors
    @start_db_transaction
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def delete(self,account_id:str,employee_id:str,shop_id:str):
        employe_todel=delete(
            Employees
        ).where(
            and_(
                Employees.id==employee_id,
                Employees.shop_id==shop_id,
                Employees.account_id==account_id,
                Employees.added_by==self.current_user_id
            )
        ).returning(Employees.id)


        is_deleted=(await self.session.execute(employe_todel)).scalar_one_or_none()

        response_content=ResponseContentTypDict(
            status=200,
            succsess=True,
            msg="Employee deleted successfully"
        )

        if not is_deleted:
            response_content=ResponseContentTypDict(
                status=404,
                msg="Error : Deleting employe data",
                description="Employee id not found",
                succsess=False
            )

            raise HTTPException(status_code=404,detail=response_content)
        
        return ORJSONResponse(
            status_code=200,
            content={"detail":response_content}
        )
    

    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get(self,shop_id:str,query:Optional[str]="",offset:Optional[int]=0,limit:Optional[int]=10):
        formatted_query:str=f"%{query.lower()}%"
        employees_toget=(
            await self.session.execute(
                select(
                    Employees.id.label("employee_id"),
                    Accounts.name.label('employee_name'),
                    Accounts.email.label("employee_email"),
                    Employees.role.label("employee_role"),
                    Employees.account_id,
                    Employees.shop_id.label("employee_shop_id"),
                    Shops.name.label("employee_shop_name"),
                    literal(True).label("is_accepted")
                )
                .join(Accounts,Accounts.id==Employees.account_id,isouter=True)
                .join(Shops,Shops.id==Employees.shop_id,isouter=True)
                .where(and_(Employees.shop_id==shop_id,or_(Employees.added_by==self.current_user_id,Employees.account_id==self.current_user_id)))
                .where(
                    or_(
                        Accounts.name.ilike(formatted_query),
                        Accounts.email.ilike(formatted_query),
                        Employees.role.ilike(formatted_query)
                    )
                )
                .offset(offset).limit(limit)
            )
        ).mappings().all()

        return {'employees':employees_toget}
    

    @catch_errors
    @verify_role(allowed_roles=[RoleEnum.SUPER_ADMIN.value])
    async def get_byid(self,account_id:str,employee_id:str,shop_id:str):
        employee_toget=(
            await self.session.execute(
                select(
                    Employees.id.label("employee_id"),
                    Accounts.name.label('employee_name'),
                    Accounts.email.label("employee_email"),
                    Employees.role.label("employee_role"),
                    Employees.account_id,
                    Employees.shop_id.label("employee_shop_id"),
                    Shops.name.label("employee_shop_name"),
                    literal(True).label("is_accepted")
    
                )
                .join(Accounts,Accounts.id==Employees.account_id,isouter=True)
                .join(Shops,Shops.id==Employees.shop_id,isouter=True)
                .where(
                    and_(
                        Employees.id==employee_id,
                        Employees.shop_id==shop_id,
                        Employees.account_id==account_id
                    )
                )
            )
        ).mappings().one_or_none()

        return {'employee':employee_toget}
