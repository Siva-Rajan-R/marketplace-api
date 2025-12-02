from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.responses import RedirectResponse
from app.middlewares.token_verification import verify_token
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.operations.crud.account_crud import AccountCrud
from app.operations.crud.employee_crud import EmployeeCrud,RoleEnum
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.auth.deb_authentication import DeBAuthentication,JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JwtTokenGenerator,JWT_TOKEN_ALGORITHM
import os
from app.database.configs.redis_config import set_redis,get_redis,unlink_redis
from pydantic import BaseModel
from icecream import ic
from dotenv import load_dotenv
load_dotenv()

FRONTEND_URL=os.getenv("FRONTEND_URL")

router=APIRouter(
    tags=["Authentication"]
)


@router.get("/auth")
async def get_login_url():
    return await DeBAuthentication.get_login_url()


@router.get('/auth/redirect')
async def get_credentials(code:str,request:Request,session=Depends(get_pg_async_session)):
    token=await DeBAuthentication.get_credentials(code=code,session=session)
    ic(token)
    url_tosend=f"{FRONTEND_URL}/shop?token={token['token']}&waiting={token['waiting']}"
    return RedirectResponse(
        url=url_tosend,
        status_code=302
    )


class AuthGetTokens(BaseModel):
    shop_id:str

@router.post("/auth/tokens")
async def get_tokens(data:AuthGetTokens,request:Request,token_data:dict=Depends(verify_token),session=Depends(get_pg_async_session)):
    role=await AccountCrud(session=session,current_user_role="").get_role(account_id=token_data['id'],shop_id=data.shop_id)
    ic(role)
    if not role:
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Getting tokens",
                description="User not found or Authenticated"
            )
        )
    
    account_info=await get_redis(f"AUTH-CRED-{token_data['id']}")
    await unlink_redis(key=[f"AUTH-CRED-{token_data['id']}"])

    if not account_info:
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
        data={'id':token_data['id'],'role':role,'shop_id':data.shop_id}
    )

    refresh_token=JwtTokenGenerator.create_token(
        jwt_alg=JWT_TOKEN_ALGORITHM,
        jwt_secret=JWT_REFRESH_TOKEN_SECRET,
        exp_day=7,
        data={'id':token_data['id'],'role':role,'shop_id':data.shop_id}
    )

    await set_redis(key=f"AUTH-{token_data['id']}",value=f"AUTH-{request.client.host}",expire=180)

    return {
        'access_token':access_token,
        'refresh_token':refresh_token,
        'user_name':account_info['name'],
        'profile_url':account_info['profile_picture']
    }



@router.get('/auth/token/new')
async def get_new_token(token_data:dict=Depends(verify_token)):
    access_token=DeBAuthentication.get_new_token(data=token_data)

    return {
        'access_token':access_token
    }



@router.get('/auth/accept/employee/{accept_id}')
async def accept_employee(accept_id:str,session:AsyncSession=Depends(get_pg_async_session)):
    employee_info=await get_redis(f'EMPLOYEE-ACCEPT-ID-{accept_id}')
    await unlink_redis(key=[f'EMPLOYEE-ACCEPT-ID-{accept_id}'])

    if not employee_info:
        raise HTTPException(
            status_code=404,
            detail=ResponseContentTypDict(
                status=404,
                msg="Error : Accepting employee",
                description="Invalid employee accept id"
            )
        )
    
    await EmployeeCrud(session=session,current_user_role=RoleEnum.SUPER_ADMIN,current_user_id="").update_accept(
        account_id=employee_info['account_id'],
        employee_id=employee_info['employee_id'],
        shop_id=employee_info['shop_id'],
        is_accepted=True
    )

    return "Your are Successfully added as a employyee to that company"