from abc import ABC, abstractmethod


class HashingModel(ABC):
    @staticmethod
    @abstractmethod
    def hash_data(password:str,*args,**kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def verify_data(hashed_password: str, plain_password: str,*args,**kwargs) -> bool:
        pass


class TokenModel(ABC):
    @staticmethod
    @abstractmethod
    def create_token(data: dict,*args,**kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def verify_token(token: str,*args,**kwargs) -> dict:
        pass


class EncryptionModel(ABC):
    @staticmethod
    @abstractmethod
    def encrypt_data(plain_data:str,*args,**kwargs) -> str:
        pass

    @staticmethod
    @abstractmethod
    def decrypt_data(encrypted_data:str,*args,**kwargs) -> str:
        pass