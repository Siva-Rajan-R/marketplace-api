from fastapi import APIRouter,Depends,Query
from app.operations.crud.shop_crud import ShopCrud,RoleEnum
from ..schemas.shop_schema import AddShopSchema,UpdateShopSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List

router=APIRouter(
    tags=["Shop CRUD"]
)

role=RoleEnum.SUPER_ADMIN.value

@router.post("/shops")
async def add_shop(data:AddShopSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await ShopCrud(
        session=session,
        current_user_role=role,
        current_user_id="5bd775fc-b292-58f6-9be8-531b64615682"
    ).add(
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no
    )

@router.put("/shops")
async def update_shops(data:UpdateShopSchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await ShopCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).update(
        shop_id=data.shop_id,
        name=data.name,
        description=data.description,
        address=data.address,
        shop_type=data.shop_type,
        gst_no=data.gst_no
    )

@router.delete("/shops/{shop_id}")
async def delete_shops(shop_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await ShopCrud(
        session=session,
        current_user_role=role,
        current_user_id="5bd775fc-b292-58f6-9be8-531b64615682"
    ).delete(
        shop_id=shop_id
    )

@router.get("/shops")
async def get_shop(session:AsyncSession=Depends(get_pg_async_session)):
    return await ShopCrud(
        session=session,
        current_user_role=role,
        current_user_id="5bd775fc-b292-58f6-9be8-531b64615682"
    ).get()

@router.get("/shops/{shop_id}")
async def get_shops_byid(shop_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await ShopCrud(
        session=session,
        current_user_role=role,
        current_user_id="9cbc6df4-ae06-58c8-af9e-9f1926e89aaa"
    ).get_byid(
        shop_id=shop_id
    )