from . import HTTPException,TokenModel,ic
from app.configs.token_config import pyjwt, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta,timezone


class JwtTokenGenerator(TokenModel):
    @staticmethod
    def create_token(data: dict, jwt_secret:str,jwt_alg:str,exp_min:int=0,exp_day:int=0,exp_sec:int=0)-> str | HTTPException:
        data['exp']=datetime.now(tz=timezone.utc)+timedelta(days=exp_day,minutes=exp_min,seconds=exp_sec)
        try:
            return pyjwt.encode(
                payload=data,
                key=jwt_secret,
                algorithm=jwt_alg
            )
        
        except HTTPException:
            raise 

        except Exception as e:
            raise HTTPException(status_code=500,detail="Error : Generating Jwt Token")


    @staticmethod
    def verify_token(token: str,jwt_secret:str,jwt_alg:str) -> dict | HTTPException:
        try:
            decoded_token = pyjwt.decode(token, key=jwt_secret, algorithms=jwt_alg)
            return decoded_token
        
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        except HTTPException:
            raise 

        except Exception as e:
            ic(f"Error : Verifying Token {e}")
            raise HTTPException(status_code=500,detail="Error : Verifying Token")