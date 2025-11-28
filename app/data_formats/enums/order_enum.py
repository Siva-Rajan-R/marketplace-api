from enum import Enum

class OrderStatusEnum(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class OrderOriginEnum(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    IN_STORE = "IN_STORE"
    PHONE = "PHONE"