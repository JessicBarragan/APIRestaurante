from fastapi import APIRouter
from servicio_pagos_domicilios.modelos.domicilio import CrearDomicilio

enrutador = APIRouter(prefix="/domicilios", tags=["Domicilios"])
base_datos_domicilios = []

@enrutador.post("/")
async def asignar_domicilio(domicilio: CrearDomicilio):
    datos = domicilio.dict()
    datos["id"] = str(len(base_datos_domicilios) + 1)
    base_datos_domicilios.append(datos)
    return {"id": datos["id"], "mensaje": "Domicilio asignado exitosamente", "datos": datos}

@enrutador.get("/")
async def obtener_domicilios():
    return base_datos_domicilios