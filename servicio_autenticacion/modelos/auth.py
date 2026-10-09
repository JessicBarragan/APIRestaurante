from pydantic import BaseModel, Field


class RegistroUsuario(BaseModel):
    nombre_completo: str = Field(..., examples=["Jessica Barragán"])
    correo: str = Field(..., examples=["jessica@gmail.com"])
    # bcrypt solo admite hasta 72 caracteres
    contrasena: str = Field(..., min_length=6, max_length=72, examples=["Clave123"])


class LoginUsuario(BaseModel):
    correo: str = Field(..., examples=["jessica@gmail.com"])
    contrasena: str = Field(..., examples=["Clave123"])
