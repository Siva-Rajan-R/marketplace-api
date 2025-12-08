from fastapi import Request, HTTPException
from app.operations.crud.shop_crud import ShopCrud
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.crud.account_crud import AsyncSession
from app.data_formats.enums.user_enum import RoleEnum
from app.data_formats.typed_dicts.auth_typdict import AuthTokenInfoTypDict,AuthRedisValueTypDict,AuthOTTInfoTypDict
from app.security.url_secret_generator import UrlSecretGenerator
from app.decoraters.crud_decoraters import catch_errors
from icecream import ic

@catch_errors
async def verify_ott(token:str,request:Request,session:AsyncSession) -> AuthTokenInfoTypDict | HTTPException:
    ic(request.url.path not in ["/auth/tokens","/shops/account"] and (request.url.path=='/shops' and request.method.lower()!="post"))
    if not token:
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Unauthorized",
                description="Unauthorized: No token provided",
                succsess=False
            )
        )
    
    token_data:AuthOTTInfoTypDict=UrlSecretGenerator.verify(token=token,validate_time_sec=100000)
    ic(token_data)

    if (request.url.path not in ["/auth/tokens","/shops/account"] and (request.url.path=='/shops' and request.method.lower()!="post")):
        ic("Hi from ulla")
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                succsess=False,
                msg="Error : Unauthorized",
                description="Not authenticated"
            )
        )
    
    if (request.url.path=='/shops' and request.method.lower()=="post"):
        shop=await ShopCrud(
            session=session,
            current_user_email='',
            current_user_id=token_data['id'],
            current_user_name=token_data['name'],
            current_user_role=RoleEnum.SUPER_ADMIN
        ).get_by_account(account_id=token_data['id'])

        ic(shop)
        if shop['shops']!=[] or shop['is_owner']==False:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    msg="Error : Denied",
                    description="Shops already exists, can't create shop at the momement",
                    succsess=False
                )
            )
    
    if token_data['ip']!=request.client.host.__str__():
         raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Network interrupted",
                succsess=False,
                description="Network interupted, Login again"
            )
        )


    data:AuthTokenInfoTypDict=AuthTokenInfoTypDict(
        email='',
        id=token_data['id'],
        name=token_data['name'],
        shop_id='',
        role=RoleEnum.SUPER_ADMIN,
        profile_pic=token_data["profile_pic"]
    )
        
        
    return data