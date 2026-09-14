from pydantic import BaseModel, Field

class CrearInsumoInventario(BaseModel):
    nombre_insumo: str = Field(..., example="Grano de Café")
    cantidad_stock: float = Field(..., example=50.0)
    unidad_medida: str = Field(..., example="Kg")
    alerta_stock_minimo: float = Field(..., example=5.0)