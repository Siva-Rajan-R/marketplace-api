from ...import BASE,JSONB,relationship,Column, String,ForeignKey,Integer,TIMESTAMP,func,Boolean


class Register(BASE):
    __tablename__="register"
    email=Column(String,primary_key=True)
    name=Column(String,nullable=False)
    shop_name=Column(String,nullable=False)
    description=Column(String,nullable=False)
    shop_type=Column(String,nullable=False)
    mobile_number=Column(String,nullable=False)

    created_at=Column(TIMESTAMP(timezone=True),server_default=func.now())