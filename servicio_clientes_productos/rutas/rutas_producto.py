
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from base_datos import obtener_db
from modelos.tablas import ProductoTabla
from modelos.producto import CrearProducto
from shared.middleware_seguridad import requerir_rol

enrutador = APIRouter(
    prefix="/productos",
    tags=["Productos / Menú"]
)


# CREATE: Registrar producto
@enrutador.post("/", status_code=status.HTTP_201_CREATED)
def registrar_producto(
    producto: CrearProducto,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    existente = db.query(ProductoTabla).filter(
        ProductoTabla.nombre == producto.nombre
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El producto ya se encuentra registrado."
        )

    nuevo_producto = ProductoTabla(
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        descripcion=producto.descripcion,
        disponible=producto.disponible
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {
        "mensaje": "Producto agregado al menú exitosamente",
        "producto": {
            "id": nuevo_producto.id,
            "nombre": nuevo_producto.nombre,
            "categoria": nuevo_producto.categoria,
            "precio": nuevo_producto.precio,
            "descripcion": nuevo_producto.descripcion,
            "disponible": nuevo_producto.disponible
        }
    }


# READ: Listar productos
@enrutador.get("/")
def obtener_productos(
    db: Session = Depends(obtener_db)
):
    return db.query(ProductoTabla).all()


# READ BY ID: Consultar producto
@enrutador.get("/{producto_id}")
def obtener_producto(
    producto_id: int,
    db: Session = Depends(obtener_db)
):
    producto = db.query(ProductoTabla).filter(
        ProductoTabla.id == producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado."
        )

    return producto


# UPDATE: Actualizar producto
@enrutador.put("/{producto_id}")
def actualizar_producto(
    producto_id: int,
    datos: CrearProducto,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    producto = db.query(ProductoTabla).filter(
        ProductoTabla.id == producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado."
        )

    existente = db.query(ProductoTabla).filter(
        ProductoTabla.nombre == datos.nombre,
        ProductoTabla.id != producto_id
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe otro producto con ese nombre."
        )

    producto.nombre = datos.nombre
    producto.categoria = datos.categoria
    producto.precio = datos.precio
    producto.descripcion = datos.descripcion
    producto.disponible = datos.disponible

    db.commit()
    db.refresh(producto)

    return {
        "mensaje": "Producto actualizado exitosamente",
        "producto": producto
    }


# DELETE: Eliminar producto
@enrutador.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(requerir_rol(["ROLE_ADMIN"]))
):
    producto = db.query(ProductoTabla).filter(
        ProductoTabla.id == producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado."
        )

    db.delete(producto)
    db.commit()

    return {
        "mensaje": "Producto eliminado exitosamente"
    }
