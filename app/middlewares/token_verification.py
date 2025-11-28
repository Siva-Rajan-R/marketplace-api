from fastapi import Request, HTTPException,Depends
from fastapi.security.http import HTTPBearer,HTTPAuthorizationCredentials
from app.configs.token_config import JWT_ACCESS_TOKEN_SECRET,JWT_REFRESH_TOKEN_SECRET,JWT_TOKEN_ALGORITHM
from app.security.token_generation import JwtTokenGenerator
from icecream import ic

bearer=HTTPBearer()

async def verify_token(request:Request,credentials:HTTPAuthorizationCredentials=Depends(bearer)) -> str:
    token=credentials.credentials
    if not token:
        raise HTTPException(status_code=401,detail="Unauthorized: No token provided")
    
    secret=JWT_ACCESS_TOKEN_SECRET
    if request.base_url.path=="/auth/token/new":
        secret=JWT_REFRESH_TOKEN_SECRET

    token_data=JwtTokenGenerator.verify_token(
        token=token,
        jwt_secret=secret,
        jwt_alg=JWT_TOKEN_ALGORITHM
    )

    ic(token_data)
    # need to implement data base verification and return that verified data

    

    return token_data