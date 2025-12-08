from ..services.email_service import DebEmailService
from ..security.url_secret_generator import UrlSecretGenerator
from ..templates.emails_template.registeration_template import (
    get_registeration_failed_email_content,
    get_registeration_verified_email_content,
    get_registration_received_email_content,
    get_user_registration_accept_email_content
)
from fastapi.requests import Request
from ..templates.emails_template.employee_template import get_employee_accept_req_email_content,get_employee_accepted_email_content
from app.security.url_secret_generator import UrlSecretGenerator
from ..database.configs.redis_config import get_redis,set_redis,unlink_redis
from .uuid_generator import generate_uuid
from icecream import ic
from pydantic import EmailStr
from typing import Optional,List,Literal
from ..data_formats.enums.shop_enum import ShopTypeEnum
from dotenv import load_dotenv
import os,orjson
load_dotenv()

BACKEND_URL=os.getenv("BACKEND_URL")
ORGANAIZATION_NAME="Marketplace"
ORGANAIZATION_YEAR=2025


# For registeration realted email senders
async def send_registeration_accept_req_email(email:EmailStr,shop_name:str,name:str,description,shop_type:ShopTypeEnum,mobile_no:str,request:Request):
    token=UrlSecretGenerator.generate(
        data={
            'email':email,
            'name':name,
            'shop_name':shop_name
        }
    )
    ic(token)
    base_url=f"{BACKEND_URL}{request.app.url_path_for("accept_register",register_secret=token)}"
    admin_email_content=get_user_registration_accept_email_content(
        email=email,
        name=name,
        shop_name=shop_name,
        description=description,
        shop_type=shop_type.value or shop_type,
        mobile_number=mobile_no,
        accept_url=f"{base_url}?method=accept",
        delete_url=f"{base_url}?method=delete"
    )

    

    organization_emails:List[EmailStr]=orjson.loads(os.getenv("ORGANIZATION_EMAILS"))

    is_sended=await DebEmailService.send(
        recivers_email=organization_emails,
        subject="Registeration accept request",
        body=admin_email_content,
        is_html=True 
    )
    
    if is_sended:
        greet_email_content=get_registration_received_email_content(
            name=name.title(),
            shop_name=shop_name,
            shop_type=shop_type.value,
            mobile_number=mobile_no,
            description=description,
            email=email
        )

        await DebEmailService.send(
            recivers_email=[email],
            subject="Registeration Successfull",
            body=greet_email_content,
            is_html=True
        )

    else:
        error_email_cnt=get_registeration_failed_email_content(
            name=name,
            description="Sorry for the inconvinince, We face some error on our side while registering your account , please try again sometimes.\nIf it persists please contact throught our customer service without hesitations 👍",
        )
        await DebEmailService.send(
            recivers_email=[email],
            subject="Registeration Unsuccessfull",
            body=error_email_cnt,
            is_html=True
        )


async def send_registeration_accepted_email(method:Literal['accept','delete'],name:str,email:str,frontend_url:str):
    if method=='accept':
        email_content=get_registeration_verified_email_content(
            name=name,
            email=email,
            login_url=f"{frontend_url}/sign-in"
        )

        await DebEmailService.send(
            recivers_email=[email],
            subject="Your account verification is done ✅",
            body=email_content,
            is_html=True
        )

    else:
        email_content=get_registeration_failed_email_content(
            name=name,
            description="""
            The personal information you provided could not be verified.

            Some of the details submitted during registration did not match our verification records.

            We detected inconsistencies in your account information.

            Your identity verification could not be completed due to incomplete or incorrect details.

            We were unable to verify your identity with the information provided.
            """
        )

        await DebEmailService.send(
            recivers_email=[email],
            subject="Your account verification failed ❌",
            body=email_content,
            is_html=True
        )

# For employee related email senders
async def send_employee_aceept_req_email(shop_name:str,email:EmailStr,employee_role:str,employee_name:str,employee_id:str,account_id:str,shop_id:str,request:Request):
    data={
        'employee_id':employee_id,
        'account_id':account_id,
        'shop_id':shop_id,
        'shop_name':shop_name,
        'employee_email':email,
        'employee_name':employee_name,
        'employee_role':employee_role
    }
    employee_accept_token=UrlSecretGenerator.generate(data=data)
    accept_url=f"{BACKEND_URL}{request.app.url_path_for("accept_employee",accept_token=employee_accept_token)}"
    email_content=get_employee_accept_req_email_content(
        shop_name=shop_name,
        role=employee_role,
        employee_name=employee_name,
        accept_url=accept_url,
    )
    await DebEmailService.send(
        recivers_email=[email],
        subject=f"Your'e invited for the shop of {shop_name}",
        body=email_content,
        is_html=True
    )

    await set_redis(key=f"EMPLOYEE-ACCEPT-ID-{employee_accept_token}",value={'employee_id':employee_id,'account_id':account_id,'shop_id':shop_id,'shop_name':shop_name},expire=500)
            

async def send_employee_accepted_email(name:str,email:str,redirect_url:str,shop_name:str,role:str):
    email_content=get_employee_accepted_email_content(
        name=name,
        email=email,
        shop_name=shop_name,
        role=role,
        dashboard_url=redirect_url
    )

    await DebEmailService.send(
        recivers_email=[email],
        subject=f"Your'e now be a employee of the {shop_name} ✅",
        body=email_content,
        is_html=True
    )