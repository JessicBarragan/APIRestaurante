from pydantic import BaseModel, Field

class CrearDomicilio(BaseModel):
    id_pedido: str
    direccion_entrega: str = Field(..., example="Calle 10 # 5-20")
    nombre_repartidor: str = Field(..., example="Juan Pérez")
    estado_envio: str = Field(default="EN CAMINO")