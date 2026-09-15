from fastapi import APIRouter
from servicio_clientes_productos.modelos.cliente import CrearCliente

enrutador = APIRouter(prefix="/clientes", tags=["Clientes"])
base_datos_clientes = []

@enrutador.post("/")echo async def registrar_cliente(cliente: CrearCliente):
    datos = cliente.dict()
    datos["id"] = str(len(base_datos_clientes) + 1)
    base_datos_clientes.append(datos)
    return {"id": datos["id"], "mensaje": "Cliente registrado exitosamente", "datos": datos}

@enrutador.get("/")echo async def obtener_clientes():
    return base_datos_clientes
