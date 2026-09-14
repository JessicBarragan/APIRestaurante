from fastapi import APIRouter
from servicio_pedidos_inventario.modelos.pedido import CrearPedido

enrutador = APIRouter(prefix="/pedidos", tags=["Pedidos"])
base_datos_pedidos = []

@enrutador.post("/")
async def registrar_pedido(pedido: CrearPedido):
    datos = pedido.dict()
    datos["id"] = str(len(base_datos_pedidos) + 1)
    base_datos_pedidos.append(datos)
    return {"id": datos["id"], "mensaje": "Pedido registrado exitosamente", "datos": datos}

@enrutador.get("/")
async def obtener_pedidos():
    return base_datos_pedidos