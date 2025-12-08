from fastapi import APIRouter,Depends,Query,Request
from app.operations.crud.account_crud import AccountCrud,RoleEnum
from ..schemas.account_schema import AddAccountSchema,UpdateAccountSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.middlewares.token_verification import verify_token
from typing import Optional,List
from app.database.configs.redis_config import unlink_redis
from .import AuthTokenInfoTypDict,AuthRedisValueTypDict

router=APIRouter(
    tags=["Accounts CRUD"]
)

role=RoleEnum.SUPER_ADMIN

@router.post("/accounts")
async def add_Account(data:AddAccountSchema,session:AsyncSession=Depends(get_pg_async_session)):
    """This route only for the marketplace organization"""
    return await AccountCrud(
        session=session,
        current_user_role=role,
        current_user_name="",
        current_user_email="",
        current_user_id=""
    ).add(
        email=data.email,
        name=data.name,
        role=RoleEnum.USER
    )

@router.put("/accounts")
async def update_Account(data:UpdateAccountSchema,session:AsyncSession=Depends(get_pg_async_session)):
    """This route only for the marketplace organization"""
    await unlink_redis(key=[f"AUTH-{""}"])
    return await AccountCrud(
        session=session,
        current_user_role=role,
        current_user_name="",
        current_user_email="",
        current_user_id=""
    ).update(
        account_id="5bd775fc-b292-58f6-9be8-531b64615682",
        email=data.email,
        name=data.name,
        role=RoleEnum.USER
    )

@router.delete("/accounts")
async def delete_account(session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    await unlink_redis(key=[f"AUTH-{token_data['id']}"])
    return await AccountCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).delete(
        account_id=token_data['id']
    )

@router.get("/accounts")
async def get_account(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session)):
    """This route only for the marketplace organization"""
    return await AccountCrud(
        session=session,
        current_user_role=role,
        current_user_name="",
        current_user_email="",
        current_user_id=""
    ).get(
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/accounts/{account_id}")
async def get_Account_byid(account_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    """This route only for the marketplace organization"""
    return await AccountCrud(
        session=session,
        current_user_role=role,
        current_user_name="",
        current_user_email="",
        current_user_id=""
    ).get_byid(
        account_id=account_id
    )