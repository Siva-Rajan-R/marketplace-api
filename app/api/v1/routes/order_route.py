from fastapi import APIRouter,Depends,Query
from app.operations.crud.order_crud import OrderCrud,RoleEnum
from ..schemas.order_schema import AddOrderSchema,UpdateOrderSchema,UpdateOrderStatus
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.middlewares.token_verification import verify_token
from typing import Optional,List

router=APIRouter(
    tags=["Orders CRUD"]
)

role=RoleEnum.ADMIN

@router.post("/orders")
async def add_order(data:AddOrderSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await OrderCrud(
        session=session,
        current_user_role=token_data['role']
    ).add(
        shop_id=data.shop_id,
        orders=data.orders,
        total_price=data.order_total_price,
        order_status=data.order_status,
        order_origin=data.order_origin,
        cur_user_id=token_data['id'],
        customer_number=data.customer_number
    )

@router.put("/orders/status")
async def update_order_status(data:UpdateOrderStatus,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await OrderCrud(
        session=session,
        current_user_role=token_data['role']
    ).update_status(
        shop_id=data.shop_id,
        order_id=data.order_id,
        order_status=data.order_status,
        order_origin=data.order_origin
    )

@router.delete("/orders/{order_id}")
async def delete_order(order_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await OrderCrud(
        session=session,
        current_user_role=token_data['role']
    ).delete(
        shop_id=token_data['shop_id'],
        order_id=order_id
    )

@router.get("/orders/shop")
async def get_orders(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await OrderCrud(
        session=session,
        current_user_role=token_data['role']
    ).get(
        shop_id=token_data['shop_id'],
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/orders/{order_id}")
async def get_order_byid(order_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await OrderCrud(
        session=session,
        current_user_role=token_data['role']
    ).get_byid(
        shop_id=token_data['shop_id'],
        order_id=order_id
    )