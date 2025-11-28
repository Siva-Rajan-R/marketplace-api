from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func



class Products(BASE):
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name=Column(String, nullable=False)
    description=Column(String, nullable=False)
    category=Column(String, nullable=False)
    barcode=Column(String, nullable=True,unique=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())