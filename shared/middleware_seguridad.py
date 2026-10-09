import jwt
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "secreto_super_seguro_taller2"
ALGORITHM = "HS256" 

seguridad_bearer = HTTPBearer() 

def obtener_usuario_actual(credenciales: HTTPAuthorizationCredentials = Depends(seguridad_bearer)):
    token = credenciales.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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