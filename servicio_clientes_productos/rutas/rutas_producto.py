from fastapi import APIRouter
from modelos.producto import CrearProducto

enrutador = APIRouter(
    prefix="/productos",
    tags=["Productos / Menú"]
)

base_datos_productos = []


@enrutador.post("/")
async def registrar_producto(producto: CrearProducto):
    datos = producto.dict()
    datos["id"] = str(len(base_datos_productos) + 1)
    base_datos_productos.append(datos)

    return {
        "id": datos["id"],
        "mensaje": "Producto agregado al menú exitosamente",
        "datos": datos
    }


@enrutador.get("/")
async def obtener_productos():
    return base_datos_productos
