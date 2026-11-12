
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from base_datos import obtener_db
from modelos.tablas import ClienteTabla
from modelos.cliente import CrearCliente
from shared.middleware_seguridad import (
    obtener_usuario_actual,
    requerir_rol
)

enrutador = APIRouter(prefix="/clientes", tags=["Clientes"])


# CREATE: Registrar cliente
@enrutador.post("/", status_code=status.HTTP_201_CREATED)
def registrar_cliente(
    cliente: CrearCliente,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    existente = db.query(ClienteTabla).filter(
        ClienteTabla.email == cliente.correo
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado."
        )

    nuevo_cliente = ClienteTabla(
        nombre=cliente.nombre_completo,
        email=cliente.correo,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return {
        "mensaje": "Cliente registrado exitosamente",
        "cliente": {
            "id": nuevo_cliente.id,
            "nombre": nuevo_cliente.nombre,
            "correo": nuevo_cliente.email,
            "telefono": nuevo_cliente.telefono,
            "direccion": nuevo_cliente.direccion
        }
    }


# READ: Listar clientes
@enrutador.get("/")
def obtener_clientes(
    db: Session = Depends(obtener_db)
):
    return db.query(ClienteTabla).all()


# READ BY ID: Consultar cliente
@enrutador.get("/{cliente_id}")
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(obtener_db)
):
    cliente = db.query(ClienteTabla).filter(
        ClienteTabla.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    return cliente


# UPDATE: Actualizar cliente
@enrutador.put("/{cliente_id}")
def actualizar_cliente(
    cliente_id: int,
    datos: CrearCliente,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    cliente = db.query(ClienteTabla).filter(
        ClienteTabla.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    correo_existente = db.query(ClienteTabla).filter(
        ClienteTabla.email == datos.correo,
        ClienteTabla.id != cliente_id
    ).first()

    if correo_existente:
        raise HTTPException(
            status_code=400,
            detail="El correo ya pertenece a otro cliente."
        )

    cliente.nombre = datos.nombre_completo
    cliente.email = datos.correo
    cliente.telefono = datos.telefono
    cliente.direccion = datos.direccion

    db.commit()
    db.refresh(cliente)

    return {
        "mensaje": "Cliente actualizado exitosamente",
        "cliente": cliente
    }


# DELETE: Eliminar cliente
@enrutador.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    cliente = db.query(ClienteTabla).filter(
        ClienteTabla.id == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado."
        )

    db.delete(cliente)
    db.commit()

    return {
        "mensaje": "Cliente eliminado exitosamente"
    }
