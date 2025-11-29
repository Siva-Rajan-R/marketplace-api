from app.configs.deb_config import DEB_AUTH_CLIENT_SECRET,DEB_AUTH_API_KEY
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from app.security.token_generation import JwtTokenGenerator
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import HTTPException
from app.class_models.auth_models import DeBAuthModel
from app.decoraters.crud_decoraters import catch_errors
import httpx
from ..crud.account_crud import AccountCrud
from app.data_formats.enums.user_enum import RoleEnum
from app.security.token_generation import JwtTokenGenerator
from app.configs.token_config import pyjwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.configs.redis_config import set_redis
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from icecream import ic

DEB_AUTH_CREDENTIALS_URL="https://deb-auth-api.onrender.com/auth/authenticated-user"
DEB_AUTH_LOGIN_URL="https://deb-auth-api.onrender.com/auth"

class DeBAuthentication(DeBAuthModel):
    http_client=httpx.AsyncClient(timeout=90)

    @catch_errors
    @staticmethod
    async def get_login_url():
        res = await DeBAuthentication.http_client.post(DEB_AUTH_LOGIN_URL,json={"apikey":DEB_AUTH_API_KEY})
        if res.status_code==200:
            return {'login_url':res.json()['login_url']}
        
        raise HTTPException(
            status_code=res.status_code,
            detail=ResponseContentTypDict(
                status=res.status_code,
                msg="Error : Getting login url",
                description=res.text,
                succsess=False
            )
        )
    
    @staticmethod
    @catch_errors
    async def get_credentials(code:str,session:AsyncSession):
        res=await DeBAuthentication.http_client.post(DEB_AUTH_CREDENTIALS_URL,json={"client_secret":DEB_AUTH_CLIENT_SECRET,"code":code})

        if res.status_code==200:
            decoded_token=pyjwt.decode(res.json()['token'],options={"verify_signature": False},algorithms="HS256")
            ic(decoded_token)
            account_obj=AccountCrud(session=session,current_user_role=RoleEnum.SUPER_ADMIN)
            account=await account_obj.verify_account_exists(account_id_email=decoded_token['email'])
            ic(account)
            if not account:
                ic("Your account need to be verify !")
                # send a email to the marketplace organization
                await session.close()
                await account_obj.add(
                    name=decoded_token['name'],
                    email=decoded_token['email'],
                    role=RoleEnum.SUPER_ADMIN
                )

                return {'token':None,'waiting':True}
            
            await set_redis(key=f"AUTH-CRED-{account['id']}",value=decoded_token,expire=190)
            token=JwtTokenGenerator.create_token(
                jwt_alg=JWT_TOKEN_ALGORITHM,
                jwt_secret=JWT_ACCESS_TOKEN_SECRET,
                exp_min=5,
                data={'id':account['id'],'is_temp':True}
            )
        
            return {
                'token':token,
                'waiting':False
            }
        
        raise HTTPException(
            status_code=res.status_code,
            detail=ResponseContentTypDict(
                status=res.status_code,
                msg="Error : Getting credentials",
                description=res.text,
                succsess=False
            )
        )
    
    @staticmethod
    @catch_errors
    def get_new_token(data:dict):
        return JwtTokenGenerator.create_token(
            jwt_alg=JWT_TOKEN_ALGORITHM,
            jwt_secret=JWT_ACCESS_TOKEN_SECRET,
            exp_min=15,
            data=data
        )

