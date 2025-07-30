from sqlalchemy import Column, Integer, String

from core.db.database import Base

class Auto(Base):
    __tablename__ = 'auto'
    
    id = Column(Integer, primary_key=True, index=True)
    auto_id = Column(Integer, index=True)
    image_url = Column(String)
    title = Column(String)
    brand = Column(String)
    model = Column(String)
    year_of_release = Column(Integer)
    mileage = Column(Integer)
    location = Column(String)
    vin = Column(string)
    price = Column(Integer)
    min_installment = Column(Integer)