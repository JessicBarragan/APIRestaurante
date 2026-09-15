from pydantic import BaseModel, Field
from typing import List

class ItemPedido(BaseModel):
    id_producto: str
    cantidad: int
    precio_unitario: float

class CrearPedido(BaseModel):
    id_cliente: str
    items: List[ItemPedido]
    monto_total: float
    estado: str = Field(default="PENDIENTE")