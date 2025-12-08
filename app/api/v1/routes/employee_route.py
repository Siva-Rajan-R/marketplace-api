from fastapi import APIRouter,Depends,Query,Request,BackgroundTasks
from app.operations.crud.employee_crud import EmployeeCrud,RoleEnum
from ..schemas.employee_schema import AddEmployeeSchema,UpdateEmployeeSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List
from app.database.configs.redis_config import unlink_redis
from app.middlewares.token_verification import verify_token
from .import AuthTokenInfoTypDict,AuthRedisValueTypDict
from app.database.models.redis_models.auth_model import AuthRedisModels

router=APIRouter(
    tags=["Employees CRUD"]
)

role=RoleEnum.SUPER_ADMIN

@router.post("/employees")
async def add_employee(data:AddEmployeeSchema,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await EmployeeCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).add(
        shop_id=token_data['shop_id'],
        email=data.email,
        name=data.name,
        role=data.role,
        bgt=bgt
    )



@router.put("/employees/role")
async def update_employee_role(data:UpdateEmployeeSchema,request:Request,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    res=await EmployeeCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).update_role(
        account_id=data.account_id,
        shop_id=token_data['shop_id'],
        employee_id=data.employee_id,
        role=data.role
    )

    await AuthRedisModels.unlink_login_info(user_id=data.account_id)

    return res

@router.delete("/employees/{account_id}/{employee_id}")
async def delete_employee(account_id:str,employee_id:str,request:Request,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    res=await EmployeeCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).delete(
        employee_id=employee_id,
        account_id=account_id,
        shop_id=token_data['shop_id']
    )

    await AuthRedisModels.unlink_login_info(user_id=account_id)

    return res

@router.get("/employees")
async def get_employee(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await EmployeeCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).get(
        shop_id=token_data['shop_id'],
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/employees/{account_id}/{employee_id}")
async def get_employee_byid(account_id:str,employee_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await EmployeeCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).get_byid(
        employee_id=employee_id,
        account_id=account_id,
        shop_id=token_data['shop_id']
    )