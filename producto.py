from pydantic import BaseModel, Field

class CrearProducto(BaseModel):
    nombre: str = Field(..., example="Café Capuchino")
    categoria: str = Field(..., example="Bebidas Calientes")
    precio: float = Field(..., example=8500.0)
    descripcion: str = Field(..., example="Café expreso con leche vaporizada")
    disponible: bool = Field(default=True)