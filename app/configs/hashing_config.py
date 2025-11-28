from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


argon2_hasher = PasswordHasher()