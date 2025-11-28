from app.configs.encryption_config import cryp_fernet,InvalidSignature
from .import ic,EncryptionModel,HTTPException
import orjson

class SymmetricEncryption(EncryptionModel):
    @staticmethod
    def encrypt_data(plain_data:any):
        try:
            encoded_data=orjson.dumps(plain_data)
            encrypted_data=cryp_fernet.encrypt(data=encoded_data)

            return encrypted_data.decode()
        except Exception as e:
            ic(f"Error : encrypting data {e}")
            raise HTTPException(status_code=500,detail="Error : encrypting data")
        
    @staticmethod
    def decrypt_data(encrypted_data:str):
        try:
            decrypted_data=cryp_fernet.decrypt(data=encrypted_data.encode())
            decoded_data=orjson.loads(decrypted_data)

            return decoded_data
        
        except InvalidSignature:
            raise HTTPException(status_code=401,detail="Decryption failed due to invalid signature")
        
        except HTTPException:
            raise 

        except Exception as e:
            ic(f"Error : decrypting data {e}")
            raise HTTPException(status_code=500,detail="Error : decrypting data")
        
