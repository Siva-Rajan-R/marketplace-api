from app.data_formats.typed_dicts.auth_typdict import AuthRedisValueTypDict
from ...configs.redis_config import get_redis,unlink_redis,set_redis
from typing import Annotated

class AuthRedisModels:

    @staticmethod
    def __login_info_key_builder(user_id:str):
        return f"AUTH-{user_id}"
    
    @staticmethod
    async def set_login_info(user_id:str,value:AuthRedisValueTypDict):
        key=AuthRedisModels.__login_info_key_builder(user_id)
        await set_redis(key=key,value=value,expire=500)

    @staticmethod
    async def get_login_info(user_id:str)->AuthRedisValueTypDict:
        key=AuthRedisModels.__login_info_key_builder(user_id)
        await get_redis(key=key)

    @staticmethod
    async def unlink_login_info(user_id:str):
        key=AuthRedisModels.__login_info_key_builder(user_id)
        await unlink_redis(key=[key])