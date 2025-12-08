from fastapi import APIRouter,Depends,Query
from app.operations.crud.shop_crud import ShopCrud,RoleEnum
from ...schemas.shop_schema import AddShopSchema,UpdateShopSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.middlewares.token_verification import verify_token
from typing import Optional,List
from ..import AuthTokenInfoTypDict,AuthRedisValueTypDict

v1_router=APIRouter(
    tags=["V1 Shop CRUD"]
)

role=RoleEnum.SUPER_ADMIN.value

@v1_router.post("/shops")
async def add_shop(data:AddShopSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).add(
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no,
        mobile_number=data.mobile_number
    )

@v1_router.put("/shops")
async def update_shops(data:UpdateShopSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).update(
        shop_id=token_data['shop_id'],
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no,
        mobile_number=data.mobile_number
    )

@v1_router.delete("/shops")
async def delete_shops(session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).delete(
        shop_id=token_data['shop_id']
    )

@v1_router.get("/shops")
async def get_shop(session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).get()


@v1_router.get("/shops/account")
async def get_shops_by_account(session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role='',
        current_user_name=token_data.get('name',""),
        current_user_email=token_data.get('email',""),
        current_user_id=token_data['id']
    ).get_by_account(account_id=token_data['id'])


@v1_router.get("/shops/shop")
async def get_shops_byid(session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data.get('name',""),
        current_user_email=token_data.get('email',""),
        current_user_id=token_data['id']
    ).get_byid(
        shop_id=token_data['shop_id']
    )
