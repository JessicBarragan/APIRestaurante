from pydantic import BaseModel, Field

class CrearPago(BaseModel):
    id_pedido: str
    monto: float
    metodo_pago: str = Field(..., example="NEQUI / EFECTIVO")
    estado: str = Field(default="COMPLETADO")