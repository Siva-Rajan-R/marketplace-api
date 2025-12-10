from fastapi import APIRouter,Depends,Request,HTTPException,BackgroundTasks
from fastapi.responses import RedirectResponse
from app.middlewares.token_verification import verify_token
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.operations.crud.account_crud import AccountCrud
from ...schemas.register_schema import RegisterationAddSchema
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.auth.deb_authentication import DeBAuthentication,JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JwtTokenGenerator,JWT_TOKEN_ALGORITHM
from app.operations.crud.register_crud import RegisterCrud
import os
from ..import AuthTokenInfoTypDict,AuthRedisValueTypDict
from app.database.models.redis_models.auth_model import AuthRedisModels
from pydantic import BaseModel
from app.data_formats.enums.user_enum import RoleEnum
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

FRONTEND_URL=os.getenv("FRONTEND_URL")

v1_router=APIRouter(
    tags=["V1 Authentication Register/Login Routes"],
    prefix='/auth'
)

@v1_router.post("/register")
async def add_Account(data:RegisterationAddSchema,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_pg_async_session)):
    ic(request.app.url_path_for('accept_register',register_secret="12345"))
    return await RegisterCrud(
        session=session,
        current_user_email='',
        current_user_name='',
        current_user_id='',
        current_user_role=RoleEnum.SUPER_ADMIN
    ).add(
        name=data.name,
        shop_name=data.shop_name,
        email=data.email,
        mobile_number=data.mobile_number,
        shop_type=data.shop_type,
        description=data.description,
        bgt=bgt,
        request=request
    )

@v1_router.get("/login")
async def get_login_url():
    return await DeBAuthentication.get_login_url()


@v1_router.get('/redirect')
async def get_credentials(code:str,request:Request,session=Depends(get_pg_async_session)):
    token=await DeBAuthentication.get_credentials(code=code,session=session,cur_ip=request.client.host.__str__())
    ic(token)
    url_tosend=f"{FRONTEND_URL}/shop?token={token['token']}&waiting={token['waiting']}"
    return RedirectResponse(
        url=url_tosend,
        status_code=302
    )


class AuthGetTokens(BaseModel):
    shop_id:str

@v1_router.post("/tokens",name="auth_tokens")
async def get_tokens(data:AuthGetTokens,request:Request,token_data:AuthTokenInfoTypDict=Depends(verify_token),session=Depends(get_pg_async_session)):
    ic(token_data,data.shop_id)
    account=await AccountCrud(session=session,current_user_role="",current_user_email="",current_user_id="",current_user_name="").verify_account_exists(account_id_email=token_data['id'],shop_id=data.shop_id)
    ic( "this your account",account)
    if not account:
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Getting tokens",
                description="User not found or Authenticated"
            )
        )
    ip=request.client.host.__str__()

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Getting tokens",
                description="Invalid token , Please sign in again"
            )
        )
    
    
    access_token=JwtTokenGenerator.create_token(
        jwt_alg=JWT_TOKEN_ALGORITHM,
        jwt_secret=JWT_ACCESS_TOKEN_SECRET,
        exp_min=15,
        data={'id':token_data['id'],'role':account['role'],'shop_id':data.shop_id}
    )

    refresh_token=JwtTokenGenerator.create_token(
        jwt_alg=JWT_TOKEN_ALGORITHM,
        jwt_secret=JWT_REFRESH_TOKEN_SECRET,
        exp_day=7,
        data={'id':token_data['id'],'role':account['role'],'shop_id':data.shop_id}
    )
    
    value_toset=AuthRedisValueTypDict(
        ip=ip,
        email=account['email'],
        name=account['name'],
    )
    
    await AuthRedisModels.set_login_info(user_id=token_data['id'],value=value_toset)


    return {
        'access_token':access_token,
        'refresh_token':refresh_token,
        'shop_id':data.shop_id,
        'user_name':account['name'],
        'profile_url':token_data.get('profile_pic')
    }



@v1_router.get('/token/new',name="auth_tokens_new")
async def get_new_token(token_data:dict=Depends(verify_token)):
    access_token=DeBAuthentication.get_new_token(data=token_data)

    return {
        'access_token':access_token
    }

