from fastapi import APIRouter,Depends,Query
from app.operations.crud.shop_crud import ShopCrud,RoleEnum
from ..schemas.shop_schema import AddShopSchema,UpdateShopSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.middlewares.token_verification import verify_token
from typing import Optional,List

router=APIRouter(
    tags=["Shop CRUD"]
)

role=RoleEnum.SUPER_ADMIN.value

@router.post("/shops")
async def add_shop(data:AddShopSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_id=token_data['id']
    ).add(
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no,
        mobile_number=data.mobile_number
    )

@router.put("/shops")
async def update_shops(data:UpdateShopSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_id=token_data['id']
    ).update(
        shop_id=data.shop_id,
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no,
        mobile_number=data.mobile_number
    )

@router.delete("/shops")
async def delete_shops(session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_id=token_data['id']
    ).delete(
        shop_id=token_data['shop_id']
    )

@router.get("/shops")
async def get_shop(session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_id=token_data['id']
    ).get()


@router.get("/shops/account")
async def get_shops_by_account(session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role='',
        current_user_id=token_data['id']
    ).get_by_account(account_id=token_data['id'])


@router.get("/shops/shop")
async def get_shops_byid(session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ShopCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_id=token_data['id']
    ).get_byid(
        shop_id=token_data['shop_id']
    )
