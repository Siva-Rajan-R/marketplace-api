from fastapi import APIRouter,Depends,Query
from app.operations.crud.product_crud import ProductCrud,RoleEnum
from ..schemas.product_schema import AddProductSchema,UpdateProductSchema
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from typing import Optional,List
from app.middlewares.token_verification import verify_token

router=APIRouter(
    tags=["Products CRUD"]
)

role=RoleEnum.ADMIN

@router.post("/products")
async def add_product(data:AddProductSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ProductCrud(
        session=session,
        current_user_role=token_data['role']
    ).add(
        name=data.name,
        barcode=data.barcode,
        description=data.description,
        category=data.category,
    )

@router.put("/products")
async def update_product(data:UpdateProductSchema,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ProductCrud(
        session=session,
        current_user_role=token_data['role']
    ).update(
        product_id=data.product_id,
        name=data.name,
        description=data.description,
        category=data.category,
        barcode=data.barcode
    )

@router.delete("/products/{product_id}/{barcode}")
async def delete_product(product_id:str,barcode:str,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ProductCrud(
        session=session,
        current_user_role=token_data['role']
    ).delete(
        product_id=product_id,
        barcode=barcode
    )


@router.get("/products")
async def get_product(q:Optional[str]=Query(""),offset:Optional[int]=Query(0),limit:Optional[int]=Query(10),session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ProductCrud(
        session=session,
        current_user_role=token_data['role']
    ).get(
        query=q,
        offset=offset,
        limit=limit
    )

@router.get("/product/{product_id}")
async def get_product_byid(product_id:str,session:AsyncSession=Depends(get_pg_async_session),token_data:dict=Depends(verify_token)):
    return await ProductCrud(
        session=session,
        current_user_role=token_data['role']
    ).get_byid(
        product_barcode_id=product_id
    )