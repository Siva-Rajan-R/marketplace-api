from typing import TypedDict,Optional
from pydantic import EmailStr


class AuthRedisValueTypDict(TypedDict):
    ip:str
    name:str
    email:EmailStr


class AuthTokenInfoTypDict(TypedDict):
    id:str
    email:EmailStr
    name:str
    shop_id:str
    role:str
    profile_pic:Optional[str]

class AuthOTTInfoTypDict(TypedDict):
    ip:str
    name:str
    id:str
    profile_pic:str

    