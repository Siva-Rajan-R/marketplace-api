from fastapi import APIRouter,Depends,Request,Query,BackgroundTasks
from app.middlewares.token_verification import verify_token
from app.database.configs.pg_config import get_pg_async_session,AsyncSession
from app.operations.crud.employee_crud import EmployeeCrud,RoleEnum
from app.operations.crud.register_crud import RegisterCrud
from app.security.url_secret_generator import UrlSecretGenerator
from app.utils.email_senders import send_registeration_accepted_email,send_employee_accepted_email
from app.configs.webpage_config import TEMPLATE
import os
from icecream import ic
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

FRONTEND_URL=os.getenv("FRONTEND_URL")

v1_router=APIRouter(
    tags=["V1 Authentication Accept Routes"],
    prefix='/auth'
)



@v1_router.get('/accept/employee/{accept_token}',name="accept_employee")
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


@v1_router.get("/accept/register/{register_secret}",name="accept_register")
async def registeration_accept_del(register_secret:str,request:Request,bgt:BackgroundTasks,method:Literal['accept','delete']=Query(...),session:AsyncSession=Depends(get_pg_async_session)):
    register_obj=RegisterCrud(
        session=session,
        current_user_email='',
        current_user_name='',
        current_user_id='',
        current_user_role=RoleEnum.SUPER_ADMIN
    )
    token_data=UrlSecretGenerator.verify(token=register_secret,validate_time_sec=6000,throw_error=False)
    ic(token_data)
    response=False

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

                response=True
        
        else:
            res=await register_obj.delete(email=token_data['email'])
            if res:
                bgt.add_task(
                    send_registeration_accepted_email,
                    method='delete',
                    name=token_data['name'],
                    email=token_data['email'],
                    frontend_url=FRONTEND_URL
                )
                
                response=True
    
    if response:
        return TEMPLATE.TemplateResponse(
            'registeration_accept_del.html',
            context={'request':request,'method_for':method,'name':res['name'],'mobile_number':res['mobile_number'],'email':res['email'],'description':res['description'],'shop_type':res['shop_type'],'shop_name':token_data['shop_name'],'redirect_url':FRONTEND_URL}
        )
    
    return TEMPLATE.TemplateResponse(
        'error_template.html',
        context={'request':request,'error_reasons':['Token Expired','User already exists or not','Invalid token','Network issues'],'redirect_url':FRONTEND_URL}
    )