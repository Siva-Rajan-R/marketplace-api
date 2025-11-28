from fastapi import APIRouter,Depends,Query
from app.operations.crud.employee_crud import EmployeeCrud,RoleEnum
from ..schemas.employee_schema import AddEmployeeSchema,UpdateEmployeeSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List

router=APIRouter(
    tags=["Employees CRUD"]
)

role=RoleEnum.SUPER_ADMIN

@router.post("/employees")
async def add_employee(data:AddEmployeeSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await EmployeeCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).add(
        shop_id=data.shop_id,
        email=data.email,
        name=data.name,
        role=RoleEnum.USER
    )

@router.put("/employees/role")
async def update_employee_role(data:UpdateEmployeeSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await EmployeeCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).update_role(
        account_id=data.account_id,
        shop_id=data.shop_id,
        employee_id=data.employee_id,
        role=data.role
    )

@router.delete("/employees/{shop_id}/{account_id}/{employee_id}")
async def delete_employee(shop_id:str,account_id:str,employee_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await EmployeeCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).delete(
        employee_id=employee_id,
        account_id=account_id,
        shop_id=shop_id
    )

@router.get("/employees")
async def get_employee(shop_id:str=Query(...),q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session)):
    return await EmployeeCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).get(
        shop_id=shop_id,
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/employees/{shop_id}/{account_id}/{employee_id}")
async def get_employee_byid(shop_id:str,account_id:str,employee_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await EmployeeCrud(
        session=session,
        current_user_role=role
    ).get_byid(
        employee_id=employee_id,
        account_id=account_id,
        shop_id=shop_id
    )