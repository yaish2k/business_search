from sqlalchemy import Column, Integer, String
from base_model import Base


class Business(Base):
    __tablename__ = "business"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    address = Column('address', String)
    phone = Column('phone', String)
