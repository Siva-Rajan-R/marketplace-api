from fastapi import APIRouter,Depends,Query
from app.operations.crud.inventory_crud import InventoryCrud,RoleEnum
from ..schemas.inventory_schema import AddInventorySchema,UpdateInventorySchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List

router=APIRouter(
    tags=["Inventory CRUD"]
)

role=RoleEnum.ADMIN

@router.post("/inventories")
async def add_inventory(data:AddInventorySchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await InventoryCrud(
        session=session,
        current_user_role=role
    ).add(
        stocks=data.stocks,
        buy_price=data.buy_price,
        sell_price=data.sell_price,
        barcode=data.bar_code,
        cur_user_id="",
        shop_id=data.shop_id,
        product_name=data.product_name,
        product_description=data.product_description,
        product_category=data.product_category,
        image_urls=data.image_urls,
        product_id=data.product_id
    )

@router.put("/inventories")
async def update_inventory(data:UpdateInventorySchema,session:AsyncSession=Depends(get_pg_async_session)):
    return await InventoryCrud(
        session=session,
        current_user_role=role
    ).update(
        inventory_id=data.inventory_id,
        stocks=data.stocks,
        buy_price=data.buy_price,
        sell_price=data.sell_price,
        barcode=data.bar_code,
        shop_id=data.shop_id,
        product_name=data.product_name,
        product_description=data.product_description,
        product_category=data.product_category,
        image_urls=data.image_urls,
        product_id=data.product_id
    )

@router.delete("/inventories/{shop_id}/{inventory_id}")
async def delete_inventory(shop_id:str,inventory_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await InventoryCrud(
        session=session,
        current_user_role=role
    ).delete(
        shop_id=shop_id,
        inventory_id=inventory_id
    )

@router.get("/inventories/{shop_id}")
async def get_inventories(shop_id:str,q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session)):
    return await InventoryCrud(
        session=session,
        current_user_role=role
    ).get(
        shop_id=shop_id,
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/inventories/{shop_id}/{inventory_id}")
async def get_inventory_byid(shop_id:str,inventory_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    return await InventoryCrud(
        session=session,
        current_user_role=role
    ).get_byid(
        shop_id=shop_id,
        inventory_id=inventory_id
    )