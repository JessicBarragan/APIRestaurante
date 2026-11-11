import os
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

# Rutas de las llaves RSA que generamos en la raíz del proyecto
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"

# Cargar las llaves físicas en memoria
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

ALGORITMO = "RS256"
MINUTOS_EXPIRACION = 60

contexto_bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encriptar_contrasena(contrasena: str) -> str:
    """Convierte '123456' en un hash irreversible."""
    return contexto_bcrypt.hash(contrasena)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Compara la contraseña escrita con el hash guardado."""
    return contexto_bcrypt.verify(contrasena_plana, contrasena_hash)


def crear_token(datos: dict) -> str:
    """Genera un token JWT firmado de forma asimétrica con la Llave Privada RSA."""
    contenido = datos.copy()
    contenido["exp"] = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    return jwt.encode(contenido, PRIVATE_KEY, algorithm=ALGORITMO)


def decodificar_token(token: str) -> dict:
    """Valida firma usando la Llave Pública RSA y expiración. Lanza excepción si el token no sirve."""
    return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITMO])