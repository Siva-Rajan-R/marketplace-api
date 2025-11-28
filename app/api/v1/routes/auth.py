from fastapi import APIRouter,Depends,Request
from fastapi.responses import RedirectResponse
from app.middlewares.token_verification import verify_token
from app.operations.auth.deb_authentication import DeBAuthentication


router=APIRouter(
    tags=["Authentication"]
)


@router.get("/auth")
async def get_login_url():
    return await DeBAuthentication.get_login_url()


@router.get('/auth/redirect')
async def get_credentials(code:str,request:Request):
    credentials=await DeBAuthentication.get_credentials(code=code)
    return RedirectResponse(
        url=str(request.base_url),
        status_code=302
    )

@router.get('/auth/token/new')
async def get_new_token(token_data:dict=Depends(verify_token)):
    return DeBAuthentication.get_new_token(data=token_data)