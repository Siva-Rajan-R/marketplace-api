from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func,Float

class Orders(BASE):
    __tablename__="orders"
    id=Column(String,primary_key=True)
    shop_id=Column(String,ForeignKey("shops.id"))
    orders=Column(JSONB,nullable=False) #{product_id:{'qty':0,'name':'bru',price:100},...}
    total_price=Column(Float,nullable=False)
    customer_number=Column(String,nullable=True)
    order_by=Column(String,nullable=False)
    status=Column(String,nullable=False)
    origin=Column(String,nullable=False)

    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())