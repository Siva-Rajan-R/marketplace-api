from fastapi import APIRouter,Depends,Query
from app.operations.crud.account_crud import AccountCrud,RoleEnum
from ..schemas.account_schema import AddAccountSchema,UpdateAccountSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List

router=APIRouter(
    tags=["Accounts CRUD"]
)

role=RoleEnum.SUPER_ADMIN

@router.post("/accounts")
async def add_Account(data:AddAccountSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await AccountCrud(
        session=session,
        current_user_role=role
    ).add(
        email=data.email,
        name=data.name,
        role=RoleEnum.USER
    )

@router.put("/accounts")
async def update_Account(data:UpdateAccountSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await AccountCrud(
        session=session,
        current_user_role=role
    ).update(
        account_id="5bd775fc-b292-58f6-9be8-531b64615682",
        email=data.email,
        name=data.name,
        role=RoleEnum.USER
    )

@router.delete("/accounts")
async def delete_employee(session:AsyncSession=Depends(get_pg_async_session)):
    return await AccountCrud(
        session=session,
        current_user_role=role
    ).delete(
        account_id="123"
    )

@router.get("/accounts")
async def get_account(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session)):
    return await AccountCrud(
        session=session,
        current_user_role=role
    ).get(
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/accounts/{account_id}")
async def get_Account_byid(account_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await AccountCrud(
        session=session,
        current_user_role=role
    ).get_byid(
        account_id=account_id
    )