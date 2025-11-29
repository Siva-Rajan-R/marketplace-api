from fastapi import Request, HTTPException,Depends
from fastapi.security.http import HTTPBearer,HTTPAuthorizationCredentials
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from app.security.token_generation import JwtTokenGenerator
from app.database.configs.redis_config import set_redis,get_redis,unlink_redis
from app.database.configs.pg_config import get_pg_async_session
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.crud.account_crud import AccountCrud,AsyncSession
from app.data_formats.enums.user_enum import RoleEnum
from icecream import ic

bearer=HTTPBearer()

async def verify_token(request:Request,credentials:HTTPAuthorizationCredentials=Depends(bearer),session:AsyncSession=Depends(get_pg_async_session)) -> dict | HTTPException:
    try:
        ic(request.url.path ,request.method.lower()=="post")
        token=credentials.credentials
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
        
        # finding the correct secret for token decode
        secret=JWT_ACCESS_TOKEN_SECRET
        if request.url.path=="/auth/token/new":
            secret=JWT_REFRESH_TOKEN_SECRET

        token_data=JwtTokenGenerator.verify_token(
            token=token,
            jwt_secret=secret,
            jwt_alg=JWT_TOKEN_ALGORITHM
        )['data']

        ic(token_data)
        
        # checking the token for temporiry , only for getting token not for other routes
        is_temp_token=token_data.get("is_temp",None)
        ic(is_temp_token)
        if is_temp_token and (request.url.path not in ["/auth/tokens","/shops/account"] and (request.url.path=='/shops' and request.method.lower()!="post")):
            raise HTTPException(
                status_code=401,
                detail=ResponseContentTypDict(
                    status=401,
                    succsess=False,
                    msg="Error : Unauthorized",
                    description="Not authenticated"
                )
            )
        
        
        is_exists_redis=await get_redis(F"AUTH-{token_data['id']}") #it returns the ip of the user based on theri account id
        ic(is_exists_redis)
        if is_exists_redis and (is_exists_redis!=f"AUTH-{request.client.host}"):
            raise HTTPException(
                status_code=401,
                detail=ResponseContentTypDict(
                    status=401,
                    msg="Error : Network interrupted",
                    succsess=False,
                    description="Network interupted, Login again"
                )
            )
        
        # verifying user only if it was not temp token and not present in redis
        if not is_temp_token and not is_exists_redis:
            role=await AccountCrud(session=session,current_user_role="").get_role(account_id=token_data['id'],shop_id=token_data['shop_id'])
            ic(role,token_data['role'])
            if not role or role!=token_data['role']:
                raise HTTPException(
                    status_code=401,
                    detail=ResponseContentTypDict(
                        status=401,
                        succsess=False,
                        msg="Error : Unauthorized",
                        description="User not authenticated"
                    )
                )
            await set_redis(key=f"AUTH-{token_data['id']}",value=f"AUTH-{request.client.host}",expire=180)
            ic("verified token via database")
        else:
            ic("verified token via redis")
            token_data['role']=RoleEnum.SUPER_ADMIN
            
        await session.close_all()
            
        return token_data
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ResponseContentTypDict(
                status=500,
                succsess=False,
                msg="Error : Internal server error ",
                description="Something went wrong , please try again later if it persist please contact support@debuggers.com"
            )
        )