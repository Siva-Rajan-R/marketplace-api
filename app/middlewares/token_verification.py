from fastapi import Request, HTTPException,Depends
from fastapi.security.http import HTTPBearer,HTTPAuthorizationCredentials
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from app.security.token_generation import JwtTokenGenerator
from app.database.models.redis_models.auth_model import AuthRedisModels
from app.database.configs.pg_config import get_pg_async_session
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict
from app.operations.crud.account_crud import AccountCrud,AsyncSession
from app.data_formats.enums.user_enum import RoleEnum
from app.data_formats.typed_dicts.auth_typdict import AuthTokenInfoTypDict,AuthRedisValueTypDict
from app.decoraters.crud_decoraters import catch_errors
from .ott_verification import verify_ott
from icecream import ic

bearer=HTTPBearer()

@catch_errors
async def verify_token(request:Request,credentials:HTTPAuthorizationCredentials=Depends(bearer),session:AsyncSession=Depends(get_pg_async_session)) -> AuthTokenInfoTypDict | HTTPException:
    async def __token_verification_handler(token:str):
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
        
        try:
            ic("Ott verification")
            token_data:AuthTokenInfoTypDict=await verify_ott(token=token,request=request,session=session)
            return {'token_data':token_data,'is_ott':True}
        except Exception as e:
            ic("Error : => ",e)
            ...
        try:
            ic("Jwt verification")
            secret=JWT_ACCESS_TOKEN_SECRET
            if request.url.path=="/auth/token/new":
                secret=JWT_REFRESH_TOKEN_SECRET

            token_data:dict=JwtTokenGenerator.verify_token(
                token=token,
                jwt_secret=secret,
                jwt_alg=JWT_TOKEN_ALGORITHM
            ).get('data',{})

            return {'token_data':token_data,'is_ott':False}
        except Exception as e:
            ic("Error : => ",e)
            ...
        
        raise HTTPException(
            status_code=401,
            detail=ResponseContentTypDict(
                status=401,
                msg="Error : Unauthorized",
                description="Invalid token, try to login !",
                succsess=False
            )
        )
    
    # getting token from header {Authorization : Bearer }
    token:str=credentials.credentials 

    # finding the correct secret for token decode
    verified_token_info=await __token_verification_handler(token=token)
    token_data:dict | AuthTokenInfoTypDict=verified_token_info['token_data']
    is_ott:bool=verified_token_info['is_ott']
    ic(token_data,is_ott)
    
    # verifying user only if it was not ott token
    extracted_acc_info=None
    if not is_ott:
        # checking the incoming account is in redis or not
        is_exists_redis:AuthRedisValueTypDict=await AuthRedisModels.get_login_info(user_id=token_data['id'])
        ic(is_exists_redis)
        if is_exists_redis and (is_exists_redis['ip']!=request.client.host.__str__()):
            is_exists_redis=None
        
        # if not in redis means we are going to check it from db and storing it to redis
        if not is_exists_redis:
            account_info=await AccountCrud(
                session=session,
                current_user_role=RoleEnum.SUPER_ADMIN,
                current_user_email="internal@api.com",current_user_id="internal userid",current_user_name="Internal user name"
            ).verify_account_exists(account_id_email=token_data['id'])

            ic(account_info,token_data['role'])
            # if the account not exists or mismatched role it will rais an error
            if not account_info or account_info['role']!=token_data['role']:
                raise HTTPException(
                    status_code=401,
                    detail=ResponseContentTypDict(
                        status=401,
                        succsess=False,
                        msg="Error : Unauthorized",
                        description="User not authenticated"
                    )
                )
            
            login_value_info=AuthRedisValueTypDict(
                ip=request.client.host.__str__(),
                name=account_info['name'],
                email=account_info['email']
            )
            await AuthRedisModels.set_login_info(user_id=token_data['id'],value=login_value_info)

            extracted_acc_info=AuthTokenInfoTypDict(
                name=account_info['name'],
                email=account_info['email'],
                id=account_info['id'],
                role=account_info['role'],
                shop_id=token_data['shop_id']
            )

            ic("verified via pg db")

        else:
            ic("verified token via redis")
            extracted_acc_info=AuthTokenInfoTypDict(
                name=is_exists_redis['name'],
                email=is_exists_redis['email'],
                id=token_data['id'],
                role=token_data['role'],
                shop_id=token_data['shop_id']
            )

    else:
        ic("which is ott token")
        extracted_acc_info=token_data

    await session.close()
        
    return extracted_acc_info
