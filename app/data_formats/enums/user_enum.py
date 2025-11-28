from enum import Enum


class RoleEnum(str,Enum):
    SUPER_ADMIN="SUPER ADMIN"
    USER="USER"
    ADMIN="ADMIN"
    STAFF="STAFF"
    MANAGER="MANAGER"