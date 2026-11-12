
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from modelos.auth import LoginUsuario, RegistroUsuario
from seguridad import (
    crear_token,
    decodificar_token,
    encriptar_contrasena,
    verificar_contrasena,
)

enrutador = APIRouter(prefix="/auth", tags=["Autenticación"])

# Base de datos temporal de usuarios
base_datos_usuarios = []

esquema_bearer = HTTPBearer()


def buscar_usuario(correo: str):
    for usuario in base_datos_usuarios:
        if usuario["correo"] == correo:
            return usuario
    return None


# REGISTRO DE USUARIOS
@enrutador.post("/registro", status_code=201)
async def registrar_usuario(datos: RegistroUsuario):

    if buscar_usuario(datos.correo):
        raise HTTPException(
            status_code=400,
            detail="Ese correo ya está registrado"
        )

    usuario = {
        "id": str(len(base_datos_usuarios) + 1),
        "nombre_completo": datos.nombre_completo,
        "correo": datos.correo,
        "contrasena_hash": encriptar_contrasena(datos.contrasena),
        "rol": "ROLE_USER"
    }

    base_datos_usuarios.append(usuario)

    return {
        "mensaje": "Usuario registrado exitosamente",
        "id": usuario["id"],
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    }


# INICIO DE SESIÓN
@enrutador.post("/login")
async def iniciar_sesion(datos: LoginUsuario):

    usuario = buscar_usuario(datos.correo)

    if not usuario or not verificar_contrasena(
        datos.contrasena,
        usuario["contrasena_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    token = crear_token({
        "sub": usuario["id"],
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# CONSULTAR PERFIL
@enrutador.get("/perfil")
async def ver_perfil(
    credenciales: HTTPAuthorizationCredentials = Depends(esquema_bearer)
):

    try:
        contenido = decodificar_token(credenciales.credentials)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token expiró, inicia sesión nuevamente"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    usuario = buscar_usuario(contenido.get("correo"))

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "id": usuario["id"],
        "nombre_completo": usuario["nombre_completo"],
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    }
