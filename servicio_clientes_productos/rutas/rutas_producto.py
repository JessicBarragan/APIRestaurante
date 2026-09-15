from fastapi import APIRouter
from servicio_clientes_productos.modelos.producto import CrearProducto

enrutador = APIRouter(prefix="/productos", tags=["Productos / Men£"])
base_datos_productos = []

@enrutador.post("/")echo async def registrar_producto(producto: CrearProducto):
    datos = producto.dict()
    datos["id"] = str(len(base_datos_productos) + 1)
    base_datos_productos.append(datos)
    return {"id": datos["id"], "mensaje": "Producto agregado al men£ exitosamente", "datos": datos}

@enrutador.get("/")echo async def obtener_productos():
    return base_datos_productos
