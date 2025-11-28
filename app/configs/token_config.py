import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv
import os
load_dotenv()

JWT_TOKEN_ALGORITHM=os.getenv("JWT_TOKEN_ALGORITHM")
JWT_ACCESS_TOKEN_SECRET=os.getenv("JWT_ACCESS_TOKEN_SECRET")
JWT_REFRESH_TOKEN_SECRET=os.getenv("JWT_REFRESH_TOKEN_SECRET")

pyjwt=jwt.PyJWT()