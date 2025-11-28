from .import HTTPException,HashingModel,ic
from app.configs.hashing_config import argon2_hasher,VerifyMismatchError


class Argon2HashingModel(HashingModel):
    @staticmethod
    def hash_data(password: str) -> str | HTTPException:
        try:
            hashed_password = argon2_hasher.hash(password)
            return hashed_password
        
        except HTTPException:
            raise 

        except Exception as e:
            ic (f"Error : hashing data {e}")
            raise HTTPException(status_code=500, detail="Error : hashing data")


    @staticmethod
    def verify_data(hashed_password: str, plain_password: str) -> bool | HTTPException:
        try:
            return argon2_hasher.verify(hashed_password, plain_password)
        
        except VerifyMismatchError:
            raise HTTPException(status_code=401, detail="Hashed-Data verification failed")
        
        except HTTPException:
            raise 

        except Exception as e:
            ic(f"Error : verifying Hased-data {e}")
            return HTTPException(status_code=500, detail="Error : verifying Hased-data")