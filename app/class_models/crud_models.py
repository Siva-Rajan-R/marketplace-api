from abc import ABC,abstractmethod
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

@dataclass(frozen=True)
class BaseCrud(ABC):
    session: AsyncSession
    
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