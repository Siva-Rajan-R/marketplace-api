from app.configs.deb_config import DEB_AUTH_CLIENT_SECRET,DEB_AUTH_API_KEY
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from app.security.token_generation import JwtTokenGenerator
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from fastapi.exceptions import HTTPException
from app.class_models.auth_models import DeBAuthModel
from app.decoraters.crud_decoraters import catch_errors
import httpx
from app.configs.token_config import pyjwt
from icecream import ic

DEB_AUTH_CREDENTIALS_URL="https://deb-auth-api.onrender.com/auth/authenticated-user"
DEB_AUTH_LOGIN_URL="https://deb-auth-api.onrender.com/auth"

class DeBAuthentication(DeBAuthModel):
    http_client=httpx.AsyncClient()

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
    async def get_credentials(code:str):
        res=await DeBAuthentication.http_client.post(DEB_AUTH_CREDENTIALS_URL,json={"client_secret":DEB_AUTH_CLIENT_SECRET,"code":code})

        if res.status_code==200:
            decoded=pyjwt.decode(res.json()['token'],options={"verify_signature": False},algorithms="HS256")
            ic(decoded)
            return res.json()
        
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
    async def get_new_token(data:dict):
        return JwtTokenGenerator.create_token(
            jwt_alg=JWT_TOKEN_ALGORITHM,
            jwt_secret=JWT_ACCESS_TOKEN_SECRET,
            exp_min=15,
            data=data
        )

