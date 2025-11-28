from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature
from dotenv import load_dotenv
import os
load_dotenv()

SYME_ENCRYPTION_SECRET=os.getenv("SYME_ENCRYPTION_SECRET","").encode()

cryp_fernet=Fernet(key=SYME_ENCRYPTION_SECRET)
