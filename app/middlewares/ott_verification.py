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
    token_url_path=request.app.url_path_for("auth_tokens")
    ic(token_url_path,request.url.path)
    ic(request.url.path not in [token_url_path,"/shops/account"] and (request.url.path=='/shops' and request.method.lower()!="post"))
    
    token_data:AuthOTTInfoTypDict=UrlSecretGenerator.verify(token=token,validate_time_sec=100000)
    ic(token_data)

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
    
    if (request.url.path not in [token_url_path,"/shops/account"] and (request.url.path=='/shops' and request.method.lower()!="post")):
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
        if len(shop['shops'])>0 or shop['is_owner']==False:
            raise HTTPException(
                status_code=409,
                detail=ResponseContentTypDict(
                    status=409,
                    msg="Error : Adding Shop",
                    description="Shops already exists, can't create shop at this momement",
                    succsess=False
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