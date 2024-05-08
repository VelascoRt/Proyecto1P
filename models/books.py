from config.database import Base
from sqlalchemy import Column, Integer, String

class Books(Base):
    __tablename__ = "books"
    
    codigo = Column(Integer, primary_key = True)
    titulo = Column(String)
    autor = Column(String)
    año = Column(String)
    categoria = Column(String)
    numeroDePaginas = Column(String)