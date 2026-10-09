import os
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

# En un proyecto real esta clave va en una variable de entorno, nunca en GitHub.
CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "clave-de-desarrollo-cambiala")
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 60

contexto_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encriptar_contrasena(contrasena: str) -> str:
    """Convierte '123456' en un hash irreversible."""
    return contexto_bcrypt.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Compara la contraseña escrita con el hash guardado."""
    return contexto_bcrypt.verify(contrasena_plana, contrasena_hash)


def crear_token(datos: dict) -> str:
    """Genera un token JWT firmado que caduca en MINUTOS_EXPIRACION."""
    contenido = datos.copy()
    contenido["exp"] = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode(contenido, CLAVE_SECRETA, algorithm=ALGORITMO)


def decodificar_token(token: str) -> dict:
    """Valida firma y expiración. Lanza excepción si el token no sirve."""
    return jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
