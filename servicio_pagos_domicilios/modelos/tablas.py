from sqlalchemy import Column, Integer, String, Float
from base_datos import Base

class PagoTabla(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    estado = Column(String(30), default="APROBADO")

class DomicilioTabla(Base):
    __tablename__ = "domicilios"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, nullable=False)
    direccion = Column(String(200), nullable=False)
    estado = Column(String(50), default="EN_CAMINO")