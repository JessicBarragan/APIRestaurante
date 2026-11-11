import jwt
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Cargar la llave pública RSA generada en la raíz del proyecto
PUBLIC_KEY_PATH = "public_key.pem"

try:
    with open(PUBLIC_KEY_PATH, "rb") as f:
        PUBLIC_KEY = f.read()
except FileNotFoundError:
    # Por si se ejecuta desde otra ruta relativa
    with open("../public_key.pem", "rb") as f:
        PUBLIC_KEY = f.read()

ALGORITHM = "RS256" 

seguridad_bearer = HTTPBearer() 

def obtener_usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(seguridad_bearer)):
    token = credenciales.credentials
    try:
        # Decodificación utilizando la llave pública y algoritmo RS256
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        rol: str = payload.get("rol")
        if usuario is None or rol is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token inválido: datos incompletos"
            )
        return {"usuario": usuario, "rol": rol}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="El token ha expirado"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token inválido o corrupto"
        )

def requerir_rol(roles_permitidos: List[str]):
    def verificacion(usuario_actual: dict = Depends(obtener_usuario_actual)):
        if usuario_actual["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"Acceso denegado. Se requiere uno de estos roles: {roles_permitidos}"
            )
        return usuario_actual
    return verificacion