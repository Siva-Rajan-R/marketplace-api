from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func,Boolean
from .employees import Employees

class Accounts(BASE):
    __tablename__="accounts"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    role=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    employee=relationship("Employees",back_populates="account",cascade="all, delete-orphan",foreign_keys=[Employees.account_id])
    shop=relationship("Shops",back_populates="account")
