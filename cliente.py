from pydantic import BaseModel, Field

class CrearCliente(BaseModel):
    nombre_completo: str = Field(..., example="Carlos Mendoza")
    correo: str = Field(..., example="carlos@gmail.com")
    telefono: str = Field(..., example="3001234567")
    direccion: str = Field(..., example="Calle 10 # 5-20")