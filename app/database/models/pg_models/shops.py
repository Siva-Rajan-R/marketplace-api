from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func,Boolean

class Shops(BASE):
    __tablename__="shops"
    id=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    address=Column(JSONB,nullable=False)
    gst_no=Column(String,nullable=True)
    type=Column(String,nullable=False)
    is_verified=Column(Boolean,nullable=False)
    account_id=Column(String,ForeignKey("accounts.id",ondelete="CASCADE"),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    account=relationship("Accounts",back_populates="shop")
    employee=relationship("Employees",back_populates="shop",cascade="all, delete-orphan")
    inventory=relationship("Inventory",back_populates="shop",cascade="all, delete-orphan")

