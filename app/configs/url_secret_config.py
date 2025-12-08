from itsdangerous import URLSafeTimedSerializer,BadTimeSignature,SignatureExpired,BadSignature
from dotenv import load_dotenv
import os
load_dotenv()

URL_TOKEN_SECRET=os.getenv("URL_TOKEN_SECRET")
URL_TOKEN_SALT=os.getenv("URL_TOKEN_SALT")

serializer=URLSafeTimedSerializer(secret_key=URL_TOKEN_SECRET,salt=URL_TOKEN_SALT)