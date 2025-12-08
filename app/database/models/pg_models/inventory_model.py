from ...import BASE,Column, String,ForeignKey,Integer,TIMESTAMP,func,relationship,JSONB,Float

class Inventory(BASE):
    __tablename__="inventory"
    id=Column(String,primary_key=True)
    stocks=Column(Integer,nullable=False)
    buy_price=Column(Float,nullable=False)
    sell_price=Column(Float,nullable=False)
    barcode=Column(String,nullable=True,unique=True)
    image_urls=Column(JSONB,nullable=True)
    added_by=Column(String,nullable=False)
    shop_id=Column(String,ForeignKey("shops.id",ondelete='CASCADE'),nullable=False)
    product_id=Column(String,ForeignKey("products.id"),nullable=False)
    
    # for ovrride the product details at shop level
    product_name=Column(String,nullable=True)
    product_description=Column(String,nullable=True)
    product_category=Column(String,nullable=True)

    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    
    

    shop=relationship("Shops",back_populates="inventory")



    