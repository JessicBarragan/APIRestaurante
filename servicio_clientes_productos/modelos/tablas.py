from sqlalchemy import Column, Integer, String, Float
from base_datos import Base

class ProductoTabla(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False)

class ClienteTabla(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    telefono = Column(String(30))