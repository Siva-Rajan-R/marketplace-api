from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func


class Employees(BASE):
    __tablename__="employees"
    id=Column(String,primary_key=True)
    account_id=Column(String,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    added_by=Column(String,ForeignKey("accounts.id",ondelete='CASCADE'),nullable=False)
    shop_id=Column(String,ForeignKey("shops.id",ondelete="CASCADE"),nullable=False)
    role=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    account=relationship("Accounts",back_populates="employee",foreign_keys=[account_id])
    added_by_acc=relationship("Accounts",foreign_keys=[added_by])
    shop=relationship("Shops",back_populates="employee")