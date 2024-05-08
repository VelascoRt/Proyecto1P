from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Categorias(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)