from fastapi import APIRouter
from servicio_pedidos_inventario.modelos.inventario import CrearInsumoInventario

enrutador = APIRouter(prefix="/inventario", tags=["Inventario"])
base_datos_inventario = []

@enrutador.post("/")
async def agregar_insumo(insumo: CrearInsumoInventario):
    datos = insumo.dict()
    datos["id"] = str(len(base_datos_inventario) + 1)
    base_datos_inventario.append(datos)
    return {"id": datos["id"], "mensaje": "Insumo registrado en el inventario", "datos": datos}

@enrutador.get("/")
async def obtener_inventario():
    return base_datos_inventario