from abc import ABC,abstractmethod
from dataclasses import dataclass


class DeBAuthModel(ABC):
    @staticmethod
    @abstractmethod
    async def get_login_url():
        ...
        
    @staticmethod
    @abstractmethod
    async def get_credentials(code:str):
        ...

    @staticmethod
    @abstractmethod
    async def get_new_token():
        ...