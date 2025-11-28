from app.database.configs.pg_config import BASE
from sqlalchemy import Column, String,ForeignKey,Integer,TIMESTAMP,func,Boolean,Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship