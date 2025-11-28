from abc import ABC, abstractmethod
from pydantic import EmailStr
from typing import List


class EmailModel(ABC):
    @staticmethod
    @abstractmethod
    def send(recivers_email:List[EmailStr],subject:str,body:str,is_html:bool) -> any:
        ...