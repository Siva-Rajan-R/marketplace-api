from fastapi import APIRouter,Depends,Query
from app.operations.crud.inventory_crud import InventoryCrud,RoleEnum
from ...schemas.inventory_schema import AddInventorySchema,UpdateInventorySchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.middlewares.token_verification import verify_token
from typing import Optional,List
from ..import AuthTokenInfoTypDict,AuthRedisValueTypDict

v1_router=APIRouter(
    tags=["V1 Inventory CRUD"]
)

role=RoleEnum.ADMIN

@v1_router.post("/inventories")
async def add_inventory(data:AddInventorySchema,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await InventoryCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).add(
        stocks=data.stocks,
        buy_price=data.buy_price,
        sell_price=data.sell_price,
        barcode=data.bar_code,
        cur_user_id=token_data['id'],
        shop_id=token_data['shop_id'],
        product_name=data.product_name,
        product_description=data.product_description,
        product_category=data.product_category,
        image_urls=data.image_urls
    )

@v1_router.put("/inventories")
async def update_inventory(data:UpdateInventorySchema,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await InventoryCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).update(
        inventory_id=data.inventory_id,
        stocks=data.stocks,
        buy_price=data.buy_price,
        sell_price=data.sell_price,
        barcode=data.bar_code,
        shop_id=token_data['shop_id'],
        product_name=data.product_name,
        product_description=data.product_description,
        product_category=data.product_category,
        image_urls=data.image_urls
    )

@v1_router.delete("/inventories/{inventory_id}")
async def delete_inventory(inventory_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await InventoryCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).delete(
        shop_id=token_data['shop_id'],
        inventory_id=inventory_id
    )

@v1_router.get("/inventories/shop")
async def get_inventories(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await InventoryCrud(
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

@v1_router.get("/inventories/{inventory_id}")
async def get_inventory_byid(inventory_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:AuthTokenInfoTypDict=Depends(verify_token)):
    return await InventoryCrud(
        session=session,
        current_user_role=token_data['role'],
        current_user_name=token_data['name'],
        current_user_email=token_data['email'],
        current_user_id=token_data['id']
    ).get_byid(
        shop_id=token_data['shop_id'],
        inventory_id=inventory_id
    )