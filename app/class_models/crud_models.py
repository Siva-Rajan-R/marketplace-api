from abc import ABC,abstractmethod
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.data_formats.enums.user_enum import RoleEnum
from pydantic import EmailStr

@dataclass(frozen=True)
class BaseCrud(ABC):
    session:AsyncSession
    current_user_role:RoleEnum
    current_user_id:str
    current_user_name:str
    current_user_email:EmailStr
    
    @abstractmethod
    async def add(self,*args,**kwargs):
        ...

    @abstractmethod
    async def update(self,*args,**kwargs):
        ...

    @abstractmethod
    async def get(self,*args,**kwargs):
        ...
    
    @abstractmethod
    async def get_byid(self,*args,**kwargs):
        ...

    @abstractmethod
    async def delete(self,*args,**kwargs):
        ...