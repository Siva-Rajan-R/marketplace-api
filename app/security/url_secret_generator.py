from app.configs.url_secret_config import serializer,SignatureExpired,BadSignature,BadTimeSignature
from . import HTTPException,ic


class UrlSecretGenerator:

    @staticmethod
    def generate(data:dict):
        try:
            token=serializer.dumps(data)
            ic(token)
            return token
        
        except Exception as e:
            ic(f"Error : generating url secreet token => {e}")
            raise HTTPException(
                status_code=500,
                detail="Error : generating url secreet token"
            )
        
    @staticmethod  
    def verify(token:str,validate_time_sec:int,throw_error:bool=True):
        try:
            data=serializer.loads(token,max_age=validate_time_sec)
            ic(data)
            return data
        
        except (BadSignature,BadTimeSignature,SignatureExpired):
            if throw_error:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )
            
            return False
        
        except Exception as e:
            ic(f"Error : Validating url secret => {e}")
            if throw_error:
                raise HTTPException(
                    status_code=500,
                    detail="Error : Validating url secret "
                )
            
            return False
