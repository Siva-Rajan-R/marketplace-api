from fastapi import APIRouter,Depends,Request,HTTPException,Query,BackgroundTasks
from fastapi.responses import RedirectResponse
from app.middlewares.token_verification import verify_token
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.operations.crud.account_crud import AccountCrud
from ..schemas.register_schema import RegisterationAddSchema
from app.operations.crud.employee_crud import EmployeeCrud,RoleEnum
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.auth.deb_authentication import DeBAuthentication,JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JwtTokenGenerator,JWT_TOKEN_ALGORITHM
from app.operations.crud.register_crud import RegisterCrud
from app.security.url_secret_generator import UrlSecretGenerator
from app.services.email_service import DebEmailService
from app.utils.email_senders import send_registeration_accepted_email,send_employee_accepted_email
from app.configs.webpage_config import TEMPLATE
from app.templates.emails_template.registeration_template import get_registeration_failed_email_content,get_registeration_verified_email_content
import os
from app.database.configs.redis_config import set_redis,get_redis,unlink_redis
from .import AuthTokenInfoTypDict,AuthRedisValueTypDict,AuthOTTInfoTypDict
from app.database.models.redis_models.auth_model import AuthRedisModels
from pydantic import BaseModel
from icecream import ic
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

FRONTEND_URL=os.getenv("FRONTEND_URL")

router=APIRouter(
    tags=["Authentication"]
)

@router.post("/auth/register")
async def add_Account(data:RegisterationAddSchema,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_pg_async_session)):
    return await RegisterCrud(
        session=session
    ).add(
        name=data.name,
        email=data.email,
        mobile_number=data.mobile_number,
        shop_type=data.shop_type,
        description=data.description,
        bgt=bgt
    )

@router.get("/auth/login")
async def get_login_url():
    return await DeBAuthentication.get_login_url()


@router.get('/auth/redirect')
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

@router.post("/auth/tokens")
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
        'user_name':token_data['name'],
        'profile_url':token_data['profile_pic']
    }



@router.get('/auth/token/new')
async def get_new_token(token_data:dict=Depends(verify_token)):
    access_token=DeBAuthentication.get_new_token(data=token_data)

    return {
        'access_token':access_token
    }



@router.get('/auth/accept/employee/{accept_token}')
async def accept_employee(accept_token:str,request:Request,bgt:BackgroundTasks,session:AsyncSession=Depends(get_pg_async_session)):
    employee_info=UrlSecretGenerator.verify(accept_token,validate_time_sec=1000,throw_error=False)

    if employee_info:
        res=await EmployeeCrud(session=session,current_user_role=RoleEnum.SUPER_ADMIN,current_user_id="",current_user_email='',current_user_name='').update_accept(
            account_id=employee_info['account_id'],
            employee_id=employee_info['employee_id'],
            shop_id=employee_info['shop_id'],
            is_accepted=True
        )

        if res:
            bgt.add_task(
                send_employee_accepted_email,
                name=employee_info['employee_name'],
                email=employee_info['employee_email'],
                redirect_url=FRONTEND_URL,
                shop_name=employee_info['shop_name'],
                role=employee_info['employee_role']
            )

            return TEMPLATE.TemplateResponse(
                'employee_accept.html',
                context={'request':request,'redirect_url':FRONTEND_URL,'email':employee_info['employee_email']}
            )
    
    return TEMPLATE.TemplateResponse(
        'error_template.html',
        context={'request':request,'error_reasons':['Token Expired','Employee already exists or not','Invalid token','Network issues'],'redirect_url':FRONTEND_URL}
    )

@router.get("/auth/accept/register/{register_secret}")
async def registeration_accept_del(register_secret:str,request:Request,bgt:BackgroundTasks,method:Literal['accept','delete']=Query(...),session:AsyncSession=Depends(get_pg_async_session)):
    register_obj=RegisterCrud(session=session)
    token_data=UrlSecretGenerator.verify(token=register_secret,validate_time_sec=6000,throw_error=False)
    ic(token_data)
    if token_data:
        if method=='accept':
            res=await register_obj.transfer(email=token_data['email'])
            
            if res:
                bgt.add_task(
                    send_registeration_accepted_email,
                    method='accept',
                    name=token_data['name'],
                    email=token_data['email'],
                    frontend_url=FRONTEND_URL
                )
                return TEMPLATE.TemplateResponse(
                    'registeration_accept_del.html',
                    context={'request':request,'method_for':method,'name':res.name,'mobile_number':res.mobile_number,'email':res.email,'description':res.description,'shop_type':res.shop_type,'redirect_url':FRONTEND_URL}
                )
            
            return TEMPLATE.TemplateResponse(
                'error_template.html',
                context={'request':request,'error_reasons':['Token Expired','User already exists or not','Invalid token','Network issues'],'redirect_url':FRONTEND_URL}
            )
        
        else:
            res=await register_obj.delete(email=token_data['email'])
            
            ic(res)
            if res:
                bgt.add_task(
                    send_registeration_accepted_email,
                    method='delete',
                    name=token_data['name'],
                    email=token_data['email'],
                    frontend_url=FRONTEND_URL
                )
                return TEMPLATE.TemplateResponse(
                    'registeration_accept_del.html',
                    context={'request':request,'method_for':method,'name':res['name'],'mobile_number':res['mobile_number'],'email':res['email'],'description':res['description'],'shop_type':res['shop_type'],'redirect_url':FRONTEND_URL}
                )
            
            return TEMPLATE.TemplateResponse(
                'error_template.html',
                context={'request':request,'error_reasons':['Token Expired','User already exists or not','Invalid token','Network issues'],'redirect_url':FRONTEND_URL}
            )
    
    return TEMPLATE.TemplateResponse(
        'error_template.html',
        context={'request':request,'error_reasons':['Token Expired','User already exists or not','Invalid token','Network issues'],'redirect_url':FRONTEND_URL}
    )